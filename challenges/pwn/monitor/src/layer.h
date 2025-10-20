
#define TERMINATE 0x100000
#define FILENAME_CONTAINS 0x1
#define OUTPUT_CONTAINS 0x2
#define INPUT_CONTAINS 0x3
#define MSG_ALERT_KEY 114514
#define MSG_LOG_KEY 1919810
#define MSG_MAX_LEN 512
#define LOG_FILE_OPEN_SUCCESS 0x10001
#define LOG_READ_SUCCESS 0x10002
#define LOG_WRITE_SUCCESS 0x10003
#define LOG_FILE_CLOSE 0x10004
#define LOG_FILE_OPEN_FAILD 0x11001
#define LOG_READ_FAILD 0x11002
#define LOG_WRITE_FAILD 0x11003
#define LOG_FILE_CLOSE_FAILD 0x11004

#define PAGESIZE 0x1000

using namespace std;

int alertMsgqid;
int logMsgqid;
int logfile = 0;

typedef struct {
    long type;
    char mtext[MSG_MAX_LEN];
} MSG;

typedef struct {
    int fd;
    int flags;
    char filename[128];
    char msg[128];
} FMSG;
static_assert(MSG_MAX_LEN > sizeof(FMSG), "MSG LEN CONFLICT.");
typedef unsigned long size_t;

void alert(long type);
void logging(long type, char* message, size_t len);
int _open(char* filename, int flags, int mode);
void _close(int fd);
int _read(int fd, char* buf, unsigned int n);
int _write(int fd, char* buf, unsigned int n);
void __buildLog(char* buf, size_t max, char* text);
void byte_to_hex(char* buf, unsigned char* data, size_t len);
void sha256(char* input, size_t len, char* hexdigest);
void * _memmem(const void *__haystack, size_t __haystacklen, const void *__needle, size_t __needlelen);
void handle(MSG msg);
void * logWoker();
void * guardWorker();
void layer_init();