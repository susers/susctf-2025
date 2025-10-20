#define _POSIX_C_SOURCE 200809L
#include <arpa/inet.h>
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <linux/openat2.h>
#include <netinet/in.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>

typedef int (*open_func_t)(const char *, int, ...);
typedef int (*openat_func_t)(int, const char *, int, ...);
typedef int (*openat2_func_t)(int, const char *, struct open_how *, size_t);
typedef int (*io_uring_setup_t)(unsigned int, void *);
typedef int (*io_uring_enter_t)(unsigned int, unsigned int, unsigned int,
                                unsigned int, void *);
typedef int (*connect_func_t)(int, const struct sockaddr *, socklen_t);

int open(const char *pathname, int flags, ...) {
  static open_func_t real_open = NULL;
  if (!real_open) {
    real_open = (open_func_t)dlsym(RTLD_NEXT, "open");
  }

  if (pathname && strstr(pathname, "flag") != NULL) {
    errno = EPERM;
    return -1;
  }

  if ((flags & O_PATH) == O_PATH) {
    errno = EPERM;
    return -1;
  }

  mode_t mode = 0;
  if (flags & O_CREAT) {
    va_list args;
    va_start(args, flags);
    mode = va_arg(args, mode_t);
    va_end(args);
    return real_open(pathname, flags, mode);
  }
  return real_open(pathname, flags);
}

int openat(int dirfd, const char *pathname, int flags, ...) {
  static openat_func_t real_openat = NULL;
  if (!real_openat) {
    real_openat = (openat_func_t)dlsym(RTLD_NEXT, "openat");
  }

  if (pathname && strstr(pathname, "flag") != NULL) {
    errno = EPERM;
    return -1;
  }

  if ((flags & O_PATH) == O_PATH) {
    errno = EPERM;
    return -1;
  }

  mode_t mode = 0;
  if (flags & O_CREAT) {
    va_list args;
    va_start(args, flags);
    mode = va_arg(args, mode_t);
    va_end(args);
    return real_openat(dirfd, pathname, flags, mode);
  }
  return real_openat(dirfd, pathname, flags);
}

int openat2(int dirfd, const char *pathname, struct open_how *how,
            size_t size) {
  typedef int (*openat2_func_t)(int, const char *, struct open_how *, size_t);
  static openat2_func_t real_openat2 = NULL;
  if (!real_openat2) {
    real_openat2 = (openat2_func_t)dlsym(RTLD_NEXT, "openat2");
  }

  if (pathname && strstr(pathname, "flag") != NULL) {
    errno = EPERM;
    return -1;
  }

  if ((how->flags & O_PATH) == O_PATH) {
    errno = EPERM;
    return -1;
  }

  return real_openat2(dirfd, pathname, how, size);
}

int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen) {
  static connect_func_t real_connect = NULL;
  if (!real_connect) {
    real_connect = (connect_func_t)dlsym(RTLD_NEXT, "connect");
  }

  if (addr->sa_family == AF_INET && addrlen >= sizeof(struct sockaddr_in)) {
    struct sockaddr_in new_addr = *(struct sockaddr_in *)addr;
    new_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    return real_connect(sockfd, (struct sockaddr *)&new_addr, addrlen);
  }

  errno = EAFNOSUPPORT;
  return -1;
}

int io_uring_setup(unsigned int entries, void *params) {
  errno = EPERM;
  return -1;
}

int io_uring_enter(unsigned int fd, unsigned int to_submit,
                   unsigned int min_complete, unsigned int flags, void *sig) {
  errno = EPERM;
  return -1;
}
