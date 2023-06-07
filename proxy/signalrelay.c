/**
	// Relay received signals to the foreground process.

	// The terminal's foreground is not accessible by processes with no
	// terminal or whose controlling terminal is not the one of interest.

	// The signal relay is performed so that terminal emulators may use
	// custom bindings to send signals to the foreground process in cases
	// where kernel based signalling is not available due to line discipline
	// changes. Naturally, this is limited to the immediate process and will
	// not propagate down to nested terminal devices without special signal
	// handling or additional escapes.
*/
#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#include <spawn.h>
#include <string.h>

extern char **environ;

static void
relay(int sig)
{
	pid_t target;

	target = tcgetpgrp(STDERR_FILENO);

	if (target != 0)
	{
		if ((pid_t) abs(target) != getpid())
			kill(target, sig);
	}
}

int
main(int argc, char *argv[])
{
	int r, stat = 0;
	pid_t focus = 0;
	posix_spawnattr_t sa;

	if (argc < 3)
	{
		fprintf(stderr, "ERROR: requires executable path and command name as arguments.\n");
		return(101);
	}

	signal(SIGHUP, relay);
	signal(SIGUSR1, relay);
	signal(SIGUSR2, relay);
	#ifdef SIGINFO
		signal(SIGINFO, relay);
	#endif

	signal(SIGINT, relay);
	signal(SIGTERM, relay);

	signal(SIGQUIT, relay);
	signal(SIGTSTP, relay);

	posix_spawnattr_init(&sa);
	posix_spawnattr_setflags(&sa, POSIX_SPAWN_RESETIDS);
	r = posix_spawn(&focus, argv[1], NULL, &sa, argv+2, environ);
	if (r != 0)
	{
		fprintf(stderr, "ERROR: %s; could not execute \"%s\".\n", strerror(r), argv[1]);
		return(102);
	}

	posix_spawnattr_destroy(&sa);
	close(STDIN_FILENO);
	close(STDOUT_FILENO);

	while (waitpid(focus, &stat, 0) != focus)
	{
		/*
			// Essentially, listening for signals to relay and wait for the
			// sole child process to exit.
		*/
		if (errno != EINTR)
			abort();
	}

	/* Forward status to caller. */
	return(WEXITSTATUS(stat));
}
