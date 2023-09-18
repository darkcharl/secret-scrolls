#!/usr/bin/env bash

grep -i root ../PAK/Public/SecretScrolls/Stats/Generated/Data/Object_SecretScrolls.txt | awk '{ print $3 "," }'
