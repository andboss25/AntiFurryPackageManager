package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"os"
	"slices"
	"strconv"
	"strings"
)

func save_to_file(filename string, data []byte) error {
	return os.WriteFile("packs/"+filename, data, 0644)
}

func make_request(content string) any {
	port := "1142"
	host_bytes, err := os.ReadFile("server.txt")
	if err != nil {
		fmt.Println("Error reading server.txt:", err)
		return nil
	}
	host := string(host_bytes[:])

	conn, err := net.Dial("tcp", host+":"+port)
	if err != nil {
		fmt.Println("Connection error:", err)
		return nil
	}
	defer conn.Close()

	fmt.Fprintf(conn, "AFPM\nFUCK FURFAGS\n"+content)

	reader := bufio.NewReader(conn)

	if strings.HasPrefix(content, "DOWNLOAD\n") {
		initMessage, err := reader.ReadString('\x00')
		if err != nil {
			fmt.Println("Package not found or undexpected error occured!")
			return nil
		}

		initMessage = strings.Trim(initMessage, "\x00\r\n")
		fileHeaders := strings.Split(initMessage, "\n")

		type fileInfo struct {
			Name string
			Size int
		}

		var files []fileInfo
		for i := 0; i < len(fileHeaders)-1; i += 2 {
			name := fileHeaders[i]
			size, err := strconv.Atoi(fileHeaders[i+1])
			if err != nil {
				fmt.Println("Invalid filesize for", name, ":", err)
				return nil
			}
			files = append(files, fileInfo{Name: name, Size: size})
		}

		fmt.Fprintf(conn, "SENDFILE\n")

		for _, file := range files {
			buf := make([]byte, file.Size)
			n, err := io.ReadFull(reader, buf)
			if err != nil {
				fmt.Println("Error reading file", file.Name, ":", err)
				return nil
			}
			err = save_to_file(file.Name, buf[:n])
			if err != nil {
				fmt.Println("Error saving file", file.Name, ":", err)
				return nil
			}
			fmt.Println("Saved file:", file.Name)
		}

		return "All files downloaded"
	} else {
		message, _ := reader.ReadString('\x00')
		return strings.Trim(message, "\x00\r\n")
	}
}

func main() {
	if len(os.Args[1:]) == 0 {
		fmt.Println("AFPM is a CLI tool. Usage:")
		fmt.Println("--download <package> -> Download a package from the server.")
		os.Exit(1)
	}

	if slices.Contains(os.Args, "--download") {
		index := slices.Index(os.Args, "--download")
		if index+1 >= len(os.Args) {
			fmt.Println("Missing package name after --download")
			os.Exit(1)
		}
		result := make_request("DOWNLOAD\n" + os.Args[index+1])
		if result != nil {
			fmt.Println(result)
		}
	} else {
		fmt.Println("Unknown arguments:", os.Args[1:])
	}
}
