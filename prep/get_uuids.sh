#!/usr/bin/env bash

sed -En 's/^(new entry "[^"]+"|data "RootTemplate" "[^"]+"|^$)/\1/p' ../PAK/Public/SecretScrolls/Stats/Generated/Data/Object_*.txt | tr -d '"' | awk '{ print $NF }'

#sed -En 's/^(new entry "[^"]+"|data "RootTemplate" "[^"]+"|^$)/\1/p' ../PAK/Public/SecretScrolls/Stats/Generated/Data/Object_*.txt | tr -d '"' | awk '{ print $NF }' | egrep '^[a-z0-9]' | sed 's/\(.*\)/"\1",/'
