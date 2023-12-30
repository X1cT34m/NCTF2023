#!/bin/bash

function docker_compose_up {
    echo "start $1"
    docker compose -f $1/docker-compose.yml up -d
}

function docker_compose_down {
    echo "stop $1"
    docker compose -f $1/docker-compose.yml down
}

function docker_volume_clean {
    echo 'clean docker volume'
    docker volume rm $(docker volume ls -qf dangling=true)
}

function start_challenge {
    for challenge in $(ls -d */)
        do
            docker_compose_up $challenge
        done
}

function stop_challenge {
    for challenge in $(ls -d */)
        do
            docker_compose_down $challenge
        done
}

function auto_restart_challenge {
    while true
        do
            start_challenge
            echo "sleep $1"
            sleep $1
            stop_challenge
            docker_volume_clean
        done
}

function print_usage {
    echo "Usage: ./run.sh <start|stop|restart|clean>"
}

if [ $# -eq 0 ]
    then
        print_usage
        exit 0
fi

if [ "$1" == "start" ]
    then
        start_challenge
elif [ "$1" == "stop" ]
    then
        stop_challenge
elif [ "$1" == "restart" ]
    then
        auto_restart_challenge $2
elif [ "$1" == "clean" ]
    then
        docker_volume_clean
else
    print_usage
fi