package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
)

type UserCreds struct {
	Username string `json:"username"`
	Password string `json:"password"`
	IsAdmin  bool
}

type SessionStore struct {
	sync.Mutex
	sessions map[string]UserCreds // sessionID -> UserCreds
}

func NewSessionStore() *SessionStore {
	return &SessionStore{sessions: make(map[string]UserCreds)}
}

type UserDB struct {
	sync.Mutex
	users map[string]UserCreds // username -> creds
}

func NewUserDB() *UserDB {
	return &UserDB{users: make(map[string]UserCreds)}
}

type Auth struct {
	AdminPassword string
	Store         *SessionStore
	UserDB        *UserDB
}

func (a *Auth) RegisterHandler(w http.ResponseWriter, r *http.Request) {
	var c UserCreds
	json.NewDecoder(r.Body).Decode(&c)
	if c.Username == "" || c.Password == "" {
		http.Error(w, "username and password required", http.StatusBadRequest)
		return
	}
	if c.Username == "admin" {
		http.Error(w, "cannot register as admin", http.StatusForbidden)
		return
	}
	a.UserDB.Lock()
	defer a.UserDB.Unlock()
	if _, exists := a.UserDB.users[c.Username]; exists {
		http.Error(w, "username already exists", http.StatusConflict)
		return
	}
	a.UserDB.users[c.Username] = c
	w.Write([]byte("register success"))
}

func (a *Auth) LoginHandler(w http.ResponseWriter, r *http.Request) {
	var c UserCreds
	json.NewDecoder(r.Body).Decode(&c)
	a.UserDB.Lock()
	user, ok := a.UserDB.users[c.Username]
	a.UserDB.Unlock()
	if ok && user.Password == c.Password {
		if user.Username == "admin" && user.Password == a.AdminPassword {
			user.IsAdmin = true
		}
		sessionID := GenRandomSeq(32)
		a.Store.Lock()
		a.Store.sessions[sessionID] = user
		a.Store.Unlock()
		http.SetCookie(w, &http.Cookie{Name: "session_id", Value: sessionID, Path: "/"})
		fmt.Fprintf(w, "user %s logged in", user.Username)
		return
	}
	http.Error(w, "invalid credentials", http.StatusUnauthorized)
}

func (a *Auth) LogoutHandler(w http.ResponseWriter, r *http.Request) {
	cookie, err := r.Cookie("session_id")
	if err != nil {
		http.Error(w, "no session, are you logged in?", http.StatusInternalServerError)
		return
	}
	a.Store.Lock()
	delete(a.Store.sessions, cookie.Value)
	a.Store.Unlock()
	w.Write([]byte("user logged out"))
}

func (a *Auth) RequireAdmin(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		cookie, err := r.Cookie("session_id")
		if err != nil {
			http.Error(w, "not logged in", http.StatusUnauthorized)
			return
		}
		a.Store.Lock()
		user, ok := a.Store.sessions[cookie.Value]
		a.Store.Unlock()
		if !ok || !user.IsAdmin {
			http.Error(w, "admin only", http.StatusForbidden)
			return
		}
		next(w, r)
	}
}
