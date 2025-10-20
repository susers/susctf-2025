package main

import (
	"crypto/rand"
	"encoding/base64"
)

func GenRandomSeq(length int) string {
	b := make([]byte, length)
	_, err := rand.Read(b)
	if err != nil {
		panic(err)
	}
	return base64.URLEncoding.EncodeToString(b)[:length]
}
