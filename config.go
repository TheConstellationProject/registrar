package main

import (
	"gopkg.in/yaml.v2"
	"io/ioutil"
)

type Config struct { // Ports are strings to avoid type casting.
	Port		string    `yaml:"port"`
	Host		string   `yaml:"host"`
	TLDs		[]string `yaml:"tlds"`
	StatPort	string	 `yaml:"statport"`
	StatHost	string	 `yaml:"stathost"`
}

var config = Config{}

func init() {
	yamlFile, err := ioutil.ReadFile("config.yml")
	if err != nil {
		panic(err)
	}

	err = yaml.Unmarshal([]byte(yamlFile), &config)
	if err != nil {
		panic(err)
	}
}
