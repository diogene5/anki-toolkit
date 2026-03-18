# Windows Permission Problems

## Permission Problems

When Anki displays "access denied" messages, certain files may have read-only attributes preventing the application from writing to them.

**Resolution steps:**

1. Open the command prompt by typing `cmd.exe` in the start bar search and pressing Enter
2. Identify your username by entering:
   ```
   whoami
   ```
3. Execute these commands, replacing `____` with your username from step 2:
   ```
   cd %APPDATA%
   icacls Anki2 /grant ____:F /t
   ```

This process restores write permissions to Anki's data directory, allowing the program to launch successfully.

## Antivirus/Firewall/Anti-Malware

Security software can trigger "permission denied" or read-only errors. To resolve this:

- Add Anki to your security software's exceptions list, or
- Temporarily disable the security application to test if it's responsible

Some users report that disabling alone didn't work; they required either an explicit exception or complete uninstallation.

## Debugging Permission Problems

For persistent issues after ruling out antivirus software, fixing permissions, and excluding OneDrive involvement, run these diagnostic commands in `cmd.exe`:

```
whoami
cd %APPDATA%
icacls Anki2 /t
```

Share the output via support ticket for further assistance.
