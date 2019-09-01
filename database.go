package main

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"github.com/dgraph-io/badger"
	"net/http"
)

var db *badger.DB
var err error

type Record struct {
	Type  string
	Name  string
	Value string
}

type Domain struct {
	Domain  string
	Token   string
	Records []Record
}

func Add(domain string, value Domain) {
	var buffer bytes.Buffer

	enc := gob.NewEncoder(&buffer)
	err := enc.Encode(value)
	if err != nil {
		panic(err)
	}

	err = db.Update(func(txn *badger.Txn) error {

		err = txn.Set([]byte(domain), []byte(buffer.Bytes()))
		return err
	})

	if err != nil {
		panic(err)
	}
}

func Get(key string) Domain {
	var out []byte
	var domain Domain

	err := db.View(func(txn *badger.Txn) error {
		item, err := txn.Get([]byte(key))
		if err != nil {
			panic(err)
		}

		err = item.Value(func(val []byte) error {
			out = append([]byte{}, val...)
			return nil
		})
		if err != nil {
			panic(err)
		}

		return nil
	})
	if err != nil {
		panic(err)
	}
	decoder := gob.NewDecoder(bytes.NewReader(out))
	err = decoder.Decode(&domain)
	if err != nil {
		panic(err)
	}

	return domain

}

func Registered(key string) bool {
	inDB := true
	_ = db.View(func(txn *badger.Txn) error {
		_, err = txn.Get([]byte(key))
		if err == badger.ErrKeyNotFound {
			inDB = false
		}
		return nil
	})
	return inDB
}

func Close() {
	db.Close()
}

func init() {
	db, err = badger.Open(badger.DefaultOptions("db"))
	if err != nil {
		panic(err)
	}

	go http.ListenAndServe(config.StatHost + ":" + config.StatPort, nil)
	fmt.Println("[DATABASE] Running stat server on " + config.StatHost + ":" + config.StatPort)
}

