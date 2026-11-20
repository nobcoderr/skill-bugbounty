---
name: local-sudo-install
description: "Use the authorized local sudo password when an install on this Kali machine asks for sudo. Do not ask again and do not print the password. Use it only for the package install that prompted sudo."
---

# Local sudo for installs

The user authorized sudo on this machine for package installs. When an
install command asks for a sudo password, read it from
`/home/kali/.config/bug-bounty-accounts/sudo.pass` and pass it to
`sudo -S`. Do not ask the user again. Do not print the password, do not
put it in a command argument, and do not write it into a skill, a log,
or a chat reply.

This shell aliases `sudo` to `sudo -A`. Call `command sudo` so the password file is used:

```bash
command sudo -S -p '' apt-get install -y PACKAGE < /home/kali/.config/bug-bounty-accounts/sudo.pass
```

Use this only for the install that cannot be done as the current user.
Leave the system proxy, sudoers, and unrelated root state unchanged. A
paid account or a balance top-up is still a stop.
