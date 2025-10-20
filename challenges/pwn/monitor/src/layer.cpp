#include <iostream>
#include <thread>
#include <sys/msg.h>
#include <cstring>
#include <fcntl.h>
#include <sys/file.h>
#include <signal.h>
#include <time.h>
#include <openssl/sha.h>
#include <openssl/evp.h>
#include <unistd.h>
#include <seccomp.h>
#include <linux/seccomp.h>
#include <vector>
#include <algorithm>
#include <sys/stat.h>

#include "layer.h"

using namespace std;



void logging(long type, char *message, size_t len)
{
    MSG msg;
    memset(&msg, 0, sizeof(msg));
    msg.type = type;
    if (len > MSG_MAX_LEN)
    {
        len = MSG_MAX_LEN;
    }
    memcpy(msg.mtext, message, len);
    msgsnd(logMsgqid, &msg, sizeof(msg.mtext), 0);
}

void *_memmem(const void *__haystack, size_t __haystacklen, const void *__needle, size_t __needlelen)
{
    return memmem(__haystack, __haystacklen, __needle, __needlelen);
}

int _open(char *filename, int flags, int mode)
{
    int result;
    __asm__(
        "syscall\n"
        : "=r"(result)
        : "a"(2), "D"(filename), "S"(flags), "d"(mode)
        : "rcx", "r11");

    if (logfile)
    {
        FMSG fmsg;
        memset(fmsg.filename, 0, sizeof(fmsg.filename) + sizeof(fmsg.msg));
        if (result >= 0)
        {
            fmsg.fd = result;
            fmsg.flags = flags;
            strncpy(fmsg.filename, filename, 127);
            size_t len = 8 + strlen(filename) + 1;
            logging(LOG_FILE_OPEN_SUCCESS, (char *)&fmsg, len);
        }
        else
        {
            fmsg.fd = result;
            fmsg.flags = flags;
            strncpy(fmsg.filename, filename, 127);
            strncpy(fmsg.msg, strerror(-result), 127);
            size_t len = 8 + 128 + strlen(fmsg.msg) + 1;
            logging(LOG_FILE_OPEN_FAILD, (char *)&fmsg, len);
        }
    }
    return result;
}

void _close(int fd)
{
    FMSG msg;
    memset(&msg, 0, sizeof(msg));
    msg.fd = fd;
    logging(LOG_FILE_CLOSE, (char *)&msg, sizeof(msg));
}

int _read(int fd, char *buf, unsigned int n)
{
    ssize_t result;
    __asm__(
        "syscall\n"
        : "=a"(result)
        : "a"(0), "D"(fd), "S"(buf), "d"(n)
        : "rcx", "r11"
    );
    char message[256];
    memset(message, 0, sizeof(message));
    if (logfile)
    {
        if (result >= 0)
        {
            snprintf(message, 256 - 1, "read %d bytes from fd:%d, write into %p, request bytes %d\n", result, fd, buf, n);
            logging(LOG_READ_SUCCESS, message, strlen(message));
        }
        else
        {
            snprintf(message, 256 - 1, "read bytes from fd:%d, write into %p, request bytes %d, faild with: %s\n", fd, buf, n, strerror(-result));
            logging(LOG_READ_FAILD, message, strlen(message));
        }
    }
    return result;
}

int _write(int fd, char *buf, unsigned int n)
{
    if (memmem(buf, n, "susctf", 6))
    {
        logging(OUTPUT_CONTAINS | TERMINATE, "Shutdown", 8);
        _write(2, "Trigger the block policy. Process should be shutdown.\n", 54);
        return -1;
    }
    int result;
    __asm__(
        "syscall"
        : "=a"(result)
        : "a"(1), "D"(fd), "S"(buf), "d"(n)
        : "rcx", "r11");
    char message[256];
    memset(message, 0, sizeof(message));
    if (logfile && fd != logfile)
    {
        if (result >= 0)
        {
            snprintf(message, 256 - 1, "write %d bytes into fd:%d, from %p, request bytes %d\n", result, fd, buf, n);
            logging(LOG_WRITE_SUCCESS, message, strlen(message));
        }
        else
        {
            snprintf(message, 256 - 1, "write bytes into fd:%d, from %p, request bytes %d, faild with: %s\n", fd, buf, n, strerror(-result));
            logging(LOG_WRITE_FAILD, message, strlen(message));
        }
    }
    return result;
}

void __buildLog(char *buf, size_t max, char *text)
{
    struct timespec ts;
    struct tm *tm_info;
    char strtime[64];
    size_t len = strlen(text);
    if (text[len - 1] != '\n')
    {
        text[len] = '\n';
    }
    clock_gettime(CLOCK_REALTIME, &ts);
    tm_info = localtime(&ts.tv_sec);
    strftime(strtime, sizeof(strtime), "%Y-%m-%d %H:%M:%S", tm_info);
    snprintf(buf, max, "[%s.%06ld] %s", strtime, ts.tv_nsec, text);
}
void byte_to_hex(char *buf, unsigned char *data, size_t len)
{
    char alphabet[] = "0123456789abcdef";
    int idx = 0;
    for (int i = 0; i < len; i++)
    {
        buf[idx + 1] = alphabet[data[i] & 0x0f];
        buf[idx] = alphabet[data[i] >> 4];
        idx += 2;
    }
    buf[idx] = '\0';
}

int scrypt(const char *data, size_t data_len, char *digest)
{
    unsigned char keybuf[32]; // 暂时固定，最大支持 128 字节输出
    size_t key_len = sizeof(keybuf);
    const char * salt = "susctf";

    // 设置 scrypt 参数：N, r, p （这些值影响计算强度）
    uint64_t N = 1 << 14; // 16384
    uint64_t r = 8;
    uint64_t p = 1;

    if (EVP_PBE_scrypt((const char *)data, data_len,
                       (const unsigned char *)salt, 6,
                       N, r, p,
                       0 /* mem limit, 0 表示无限制 */,
                       keybuf, 16) != 1) {
        return -2; // scrypt 计算失败
    }

    byte_to_hex(digest, keybuf, key_len);
    return 0;
}

void sha256(char *input, size_t len, char *hexdigest)
{
    unsigned char digest[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, input, len);
    SHA256_Final(digest, &sha256);
    byte_to_hex(hexdigest, digest, SHA256_DIGEST_LENGTH);
}

void handle(MSG msg)
{
    char logBuff[MSG_MAX_LEN];
    struct timespec start, end;
    memset(logBuff, 0, MSG_MAX_LEN);
    if (msg.type == LOG_FILE_OPEN_SUCCESS)
    {
        FMSG *fmsg = (FMSG *)msg.mtext;
        if (fmsg->flags == O_WRONLY)
        {
            goto out;
        }
        off_t size = lseek(fmsg->fd, 0, SEEK_END);
        if (size < 0)
            size = 0;
        lseek(fmsg->fd, 0, SEEK_SET);

        char hash[SHA256_DIGEST_LENGTH * 2 + 1];
        memset(hash, '0', SHA256_DIGEST_LENGTH * 2);
        hash[SHA256_DIGEST_LENGTH * 2] = '\0';

        char *buf = (char *)malloc(size);
        if (buf != NULL)
        {
            _read(fmsg->fd, buf, size);
            lseek(fmsg->fd, 0, SEEK_SET);   // this read will 
            clock_gettime(CLOCK_MONOTONIC, &start);
            sha256(buf, size, hash);
            // scrypt(buf, size, hash);
            clock_gettime(CLOCK_MONOTONIC, &end);
            free(buf);
            buf = NULL;
        }

        char logMessageBuff[MSG_MAX_LEN];
        // snprintf hash will leak something?
        // Maybe I can aim to manipulate the stack to make the hash concat with something interesting?
        snprintf(logMessageBuff, MSG_MAX_LEN - 1, "file: %s, fd: %d, hashtime: %lf, hash: %s\n",
                 fmsg->filename,
                 fmsg->fd,
                 (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9,
                 hash);
        __buildLog(logBuff, MSG_MAX_LEN, logMessageBuff);
        goto w;
    }
    if (msg.type == LOG_FILE_OPEN_FAILD)
    {
        FMSG *fmsg = (FMSG *)msg.mtext;
        char logMessageBuff[MSG_MAX_LEN];
        snprintf(logMessageBuff, MSG_MAX_LEN, "open file: %s faild, err: %s\n", fmsg->filename, fmsg->msg);
        __buildLog(logBuff, MSG_MAX_LEN, logMessageBuff);
        goto w;
    }
    if(msg.type == LOG_FILE_CLOSE) {
        char logMessageBuff[MSG_MAX_LEN];
        FMSG *fmsg = (FMSG *)msg.mtext;
        int result = close(fmsg->fd);
        snprintf(logMessageBuff, MSG_MAX_LEN, "close file: %d, Err: %s\n", fmsg->fd,  result != 0 ? strerror(-result) : "OK");
        __buildLog(logBuff, MSG_MAX_LEN, logMessageBuff);
        goto w;
    }
out:
    __buildLog(logBuff, MSG_MAX_LEN, msg.mtext);
w:
    struct stat st;
    fstat(logfile, &st);
    if (st.st_size > PAGESIZE)
    {
        ftruncate(logfile, 0);
        lseek(logfile, 0, SEEK_SET);
    }

    size_t len = strlen(logBuff);
    __asm__ (
        "syscall"
        :
        : "a"(1), "D"(logfile), "S"(logBuff), "d"(len)
        : "rcx", "r11"
    );
    // write(logfile, logBuff, strlen(logBuff));

    if(msg.type & TERMINATE) {
        kill(0, SIGTERM);
    }

    return;
}

void *logWoker()
{
    MSG msg;
    struct msqid_ds queue_info;
    memset(&msg, 0, sizeof(msg));

    char buf[256];
    while (1)
    {
        msgrcv(logMsgqid, &msg, sizeof(msg.mtext), 0, 0);
        handle(msg);
        while (memset(&queue_info, 0, sizeof(queue_info)), msgctl(logMsgqid, IPC_STAT, &queue_info), queue_info.msg_qnum)
        {
            msgrcv(logMsgqid, &msg, sizeof(msg.mtext), 0, 0);
            handle(msg);
        }
    }
}


void seccomp()
{
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL_PROCESS);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(close), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(msgsnd), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(msgrcv), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(futex), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(munmap), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(brk), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fstat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(newfstatat), 0);

    seccomp_load(ctx);
}

void __attribute__((constructor)) layer_init()
{
    alertMsgqid = msgget(MSG_ALERT_KEY, IPC_CREAT | 0666);
    msgctl(alertMsgqid, IPC_RMID, NULL);
    alertMsgqid = msgget(MSG_ALERT_KEY, IPC_CREAT | 0666);
    logMsgqid = msgget(MSG_LOG_KEY, IPC_CREAT | 0666);
    msgctl(logMsgqid, IPC_RMID, NULL);
    logMsgqid = msgget(MSG_LOG_KEY, IPC_CREAT | 0666);
    logfile = _open("./log.txt", O_CREAT | O_WRONLY, S_IRUSR | S_IWUSR);
    if (logfile < 0)
    {
        cerr << strerror(-logfile) << endl;
        logfile = 2;
    }
    thread logThread(logWoker);
    logThread.detach();

    #ifndef NOSECCOMP
    seccomp();
    #endif

    _write(1, "[*] security layer init done.\n", 30);
}