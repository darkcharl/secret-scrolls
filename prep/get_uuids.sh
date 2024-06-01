#!/usr/bin/env bash

sed -En 's/^(new entry "[^"]+"|data "RootTemplate" "[^"]+"|^$)/\1/p' ../PAK/Public/SecretScrolls/Stats/Generated/Data/Object_SecretScrolls.txt | tr -d '"' | awk '{ print $NF }'

