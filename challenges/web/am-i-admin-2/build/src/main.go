package main

import (
	"log"
	"net/http"
)

const PORT_STR = ":8080"

func main() {
	adminPassword := GenRandomSeq(16)
	log.Printf("Admin password: %s\n", adminPassword)
	adminUserCreds := UserCreds{
		Username: "admin",
		Password: adminPassword,
		IsAdmin:  true,
	}

	store := NewSessionStore()
	userDB := NewUserDB()
	userDB.Lock()
	userDB.users["admin"] = adminUserCreds
	userDB.Unlock()
	auth := &Auth{
		AdminPassword: adminPassword,
		Store:         store,
		UserDB:        userDB,
	}

	http.HandleFunc("/register", auth.RegisterHandler)
	http.HandleFunc("/login", auth.LoginHandler)
	http.HandleFunc("/logout", auth.LogoutHandler)
	http.HandleFunc("/run", auth.RequireAdmin(RunCommandHandler))

	log.Printf("Server running on %s\n", PORT_STR)
	log.Fatal(http.ListenAndServe(PORT_STR, nil))
}
