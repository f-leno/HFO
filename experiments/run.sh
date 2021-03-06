#!/bin/bash

echo "[$(date +"%Y-%m-%d_%H:%M:%S")] RUNNING HFO EXPERIMENT"
echo "[$(date +"%Y-%m-%d_%H:%M:%S")] PARSING ARGUMENTS"

for i in "$@"
do
  case $i in
    -r=*|--runs=*)
    RUNS="${i#*=}"
    shift
    ;;
    -t=*|--trials=*)
    TRIALS="${i#*=}"
    shift
    ;;
    -f=*|--max-frames-per-trial=*)
    MAX_FRAMES="${i#*=}"
    shift
    ;;
    -a=*|--agent=*)
    AGENT="${i#*=}"
    shift
    ;;
    -o=*|--offense-agents=*)
    OFFENSE_AGENTS="${i#*=}"
    shift
    ;;
    -d=*|--defense-agents=*)
    DEFENSE_AGENTS="${i#*=}"
    shift
    ;;
    -m=*|--mode=*)
    MODE="${i#*=}"
    shift
    ;;
    -i=*|--evaluation_interval=*)
    INTERVAL="${i#*=}"
    shift
    ;;
    -e=*|--evaluation_duration=*)
    DURATION="${i#*=}"
    shift
    ;;
    -s=*|--seed=*)
    SEED="${i#*=}"
    shift
    ;;
    -p=*|--port=*)
    PORT="${i#*=}"
    shift
    ;;
    -x=*|--parallel_server=*)
    PARALLEL_SERVER="${i#*=}"
    shift
    ;;
    -u=*|--max_untouched=*)
    MAX_UNTOUCHED="${i#*=}"
    shift
    ;;
  esac
  shift
done

if [ -z "${RUNS+x}" ]; then
  RUNS=1
fi
if [ -z "${TRIALS+x}" ]; then
  TRIALS=10
fi
if [ -z "${MAX_FRAMES+x}" ]; then
  MAX_FRAMES=100
fi
if [ -z "${AGENT+x}" ]; then
  AGENT="Dummy"
fi
if [ -z "${OFFENSE_AGENTS+x}" ]; then
  OFFENSE_AGENTS=3
fi
if [ -z "${DEFENSE_AGENTS+x}" ]; then
  DEFENSE_AGENTS=1
fi
if [ -z "${MODE+x}" ]; then
  MODE="--headless"
  # headless, no-sync (watching in slow pace),
fi
if [ -z "${INTERVAL+x}" ]; then
  INTERVAL=5
fi
if [ -z "${DURATION+x}" ]; then
  DURATION=5
fi
if [ -z "${SEED+x}" ]; then
  SEED=12345
fi
if [ -z "${PORT+x}" ]; then
  PORT=12345
fi
if [ -z "${PARALLEL_SERVER+x}" ]; then
  PARALLEL_SERVER=1
fi
if [ -z "${MAX_UNTOUCHED+x}" ]; then
  MAX_UNTOUCHED=50
fi


#Now the number of trials is incremented to take into account how many
# evaluation trials will be carried out
((EVAL_COUNT=${TRIALS}/${INTERVAL}+1))
((EVAL_TRIALS=${EVAL_COUNT}*${DURATION}))
((TRIALS_TOTAL=${TRIALS}+${EVAL_TRIALS}+1))

START_TIME=$SECONDS

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

for ((server=0; server<${PARALLEL_SERVER}; server++ ))
do
  _now=$(date +"%Y_%m_%d-%H.%M.%S")
  _dir[${server}]="${BASE_DIR}/EVAL/${_now}_${AGENT}_${PARALLEL_SERVER}_${RUNS}/"
  mkdir -p ${_dir[${server}]};

  EXPERIMENT_LOG[${server}]="${_dir[${server}]}__EXPERIMENT_LOG"
  touch "${EXPERIMENT_LOG[${server}]}"
  echo "[$(date +"%Y-%m-%d_%H:%M:%S")] START EXPERIMENT" >> ${EXPERIMENT_LOG[${server}]}
  echo "=====================================" >> ${EXPERIMENT_LOG[${server}]}
  echo \
  "./experiments/run.sh\
    --runs=${RUNS} --trials=${TRIALS}\
    --max-frames-per-trial=${MAX_FRAMES}\
    --max_untouched=${MAX_UNTOUCHED}\
    --agent=${AGENT}\
    --offense-agents=${OFFENSE_AGENTS}\
    --defense-agents=${DEFENSE_AGENTS}\
    --mode=${MODE}\
    --evaluation_interval=${INTERVAL}\
    --evaluation_duration=${DURATION}\
    --seed=${SEED}\
    --port=${PORT}\
    --parallel_server=${PARALLEL_SERVER}" >> ${EXPERIMENT_LOG[${server}]}
  echo "=====================================" >> ${EXPERIMENT_LOG[${server}]}
  echo "[$(date +"%Y-%m-%d_%H:%M:%S")] GET BASE DIRECTORY: ${BASE_DIR}" >> ${EXPERIMENT_LOG[${server}]}
  echo "[$(date +"%Y-%m-%d_%H:%M:%S")] MAKE LOG DIRECTORY: ${_dir[${server}]}" >> ${EXPERIMENT_LOG[${server}]}
  sleep 2
done




for ((run=1; run<=${RUNS}; run++ ))
do
  echo "[$(date +"%Y-%m-%d_%H:%M:%S")] Starting RUN ${run}"
  killall -9 rcssserver
  for ((server=0; server<${PARALLEL_SERVER}; server++ ))
  do
    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] STARTING RUN ${run} ==================" >> ${EXPERIMENT_LOG[${server}]}
    sleep 2
    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] STARTING HFO SERVER" >> ${EXPERIMENT_LOG[${server}]}
    ((HFO_PORT[${server}]=${PORT}+5*${server}))
    SERVER_LOG="${_dir[${server}]}_${server}_${run}_SERVER_LOG"
    touch "${SERVER_LOG}"
    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] STARTING HFO SERVER" >> ${SERVER_LOG}
    echo "=====================================" >> ${SERVER_LOG}
    echo \
    "./bin/HFO\
    --port ${HFO_PORT[${server}]}\
    --log-dir ${_dir[${server}]}\
    --offense-agents ${OFFENSE_AGENTS}\
    --defense-npcs ${DEFENSE_AGENTS}\
    --trials ${TRIALS_TOTAL}\
    --frames-per-trial ${MAX_FRAMES}\
    --untouched-time ${MAX_UNTOUCHED}\
    --seed ${SEED}\
    ${MODE}\
    --fullstate 2>&1 >> ${SERVER_LOG} &" >> ${SERVER_LOG}
    echo "=====================================" >> ${SERVER_LOG}
    #echo "XXXXXXXXXXXXXX SERVER ${server} CALL START"
    ./bin/HFO \
    --port "${HFO_PORT[${server}]}" \
    --log-dir "${_dir[${server}]}" \
    --offense-agents "${OFFENSE_AGENTS}" \
    --defense-npcs "${DEFENSE_AGENTS}" \
    --trials "${TRIALS_TOTAL}" \
    --frames-per-trial "${MAX_FRAMES}" \
    --untouched-time "${MAX_UNTOUCHED}" \
    --seed "${SEED}" \
    "${MODE}" \
    --fullstate 2>&1 >> ${SERVER_LOG} &
    #echo "[$(date +"%Y-%m-%d_%H:%M:%S")] SERVER ${server} CA"
    # maybe add:
    #--ball-x-min 0.4 \
    #--ball-x-max 0.5 \
    # instead of headless: --no-sync \
    HFO_PID_SERVER[${server}]=$!
    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] HFO SERVER PID: ${HFO_PID_SERVER[${server}]}" >> ${EXPERIMENT_LOG[${server}]}
    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] HFO SERVER PID: ${HFO_PID_SERVER[${server}]}"
  done
  echo "[$(date +"%Y-%m-%d_%H:%M:%S")] ${PARALLEL_SERVER} SERVER SHOULD BE RUNNING NOW"
  sleep 10

  for ((agent=1; agent<=${OFFENSE_AGENTS}; agent++ ))
  do
    for ((server=0; server<${PARALLEL_SERVER}; server++ ))
    do
      AGENT_LOG="${_dir[${server}]}_${server}_${run}_AGENT_${agent}_LOG"
      AGENT_RESULTS="${_dir[${server}]}_${server}_${run}_AGENT_${agent}_RESULTS"
      touch "${AGENT_LOG}"
      echo "[$(date +"%Y-%m-%d_%H:%M:%S")] STARTING AGENT ${server}_${agent}" >> ${EXPERIMENT_LOG[${server}]}
      echo "[$(date +"%Y-%m-%d_%H:%M:%S")] STARTING AGENT ${server}_${agent}" >> ${AGENT_LOG}
      echo "=====================================" >> ${AGENT_LOG}
      echo \
      "${BASE_DIR}/experiment.py -p ${HFO_PORT[${server}]} -a ${AGENT} -i ${INTERVAL} -d\
      ${DURATION} -t ${TRIALS} -l ${AGENT_RESULTS} -s ${SEED}\
      >> ${AGENT_LOG} & >> ${AGENT_LOG}" >> ${EXPERIMENT_LOG[${server}]}
      echo "=====================================" >> ${AGENT_LOG}
      #echo "XXXXXXXXXXXXXX AGENT ${server}_${agent} CALL START"
      "${BASE_DIR}"/experiment.py -p "${HFO_PORT[${server}]}" -a "${AGENT}" -i "${INTERVAL}" -d \
      "${DURATION}" -t "${TRIALS}" -l "${AGENT_RESULTS}" -s "${SEED}"\
      2>&1 >> ${AGENT_LOG} &
      HFO_PID_AGENT[${agent}]=$!
      echo "[$(date +"%Y-%m-%d_%H:%M:%S")] AGENT ${server}_${agent} RUNNING [PID=${HFO_PID_AGENT[${agent}]}]"
      sleep 5
    done
    ((agent_count=${PARALLEL_SERVER}*${agent}))
    # check all existing agent pids
    for AGENT_PID in "${HFO_PID_AGENT[@]}"                  
    do
      if  ps -p ${AGENT_PID} > /dev/null; then
        echo "[$(date +"%Y-%m-%d_%H:%M:%S")] AGENT [${AGENT_PID}] SHOULD BE RUNNING"
      else
        echo "[$(date +"%Y-%m-%d_%H:%M:%S")] OH NO! AGENT DIED [PID=${AGENT_PID}]"
        for AGENT_PID_TO_KILL in "${HFO_PID_AGENT[@]}"                  
        do
          echo "[$(date +"%Y-%m-%d_%H:%M:%S")] KILLING AGENT [PID=${AGENT_PID_TO_KILL}]"
          kill -9 ${AGENT_PID_TO_KILL}
        done
        echo "[$(date +"%Y-%m-%d_%H:%M:%S")] KILLING ALL RCSSSERVER"
        killall -9 rcssserver
        for ((server_to_kill=0; server_to_kill<${PARALLEL_SERVER}; server_to_kill++ ))
        do
          echo "[$(date +"%Y-%m-%d_%H:%M:%S")] KILLING SERVER ${server_to_kill} [PID=${HFO_PID_SERVER[${server_to_kill}]}]"
          kill -9 ${HFO_PID_SERVER[${server_to_kill}]}
          echo "[$(date +"%Y-%m-%d_%H:%M:%S")] DELETE LOGS: ${_dir[${server_to_kill}]}"
          #rm -rf ${_dir[${server_to_kill}]}
        done
        ELAPSED_TIME=$(($SECONDS - $START_TIME))                                                                            
        echo "[$(date +"%Y-%m-%d_%H:%M:%S")] ENDING PROGRAM [DURATION=${ELAPSED_TIME}s]"
        unset HFO_PID_AGENT
        unset HFO_PID_SERVER
        sleep 60
        # do this run again
        (( run-- ))
        continue 4

        #trap "kill -TERM -$$" SIGINT
        #wait
        #exit 1
      fi                                                                                                                                                 
    done
    #sleep 10
  done

  for ((server=0; server<${PARALLEL_SERVER}; server++ ))
  do
    wait ${HFO_PID_SERVER[${server}]}
    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] SHUTTING DOWN SERVER ${server} AND CLEANING UP" >> ${EXPERIMENT_LOG[${server}]}
    #sleep 2
    #kill -9 rcssserver  >> ${EXPERIMENT_LOG}
    mv -v "${_dir[${server}]}"incomplete.hfo "${_dir[${server}]}"incomplete_"${run}".hfo >> ${EXPERIMENT_LOG[${server}]}
    ELAPSED_TIME=$(($SECONDS - $START_TIME))                                                                            
    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] END EXPERIMENT [DURATION=${ELAPSED_TIME}s]" >> ${EXPERIMENT_LOG[${server}]}
    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] END EXPERIMENT [DURATION=${ELAPSED_TIME}s]"
  done                                                               
  unset HFO_PID_AGENT
  unset HFO_PID_SERVER
  sleep 60
done

for ((server=0; server<${PARALLEL_SERVER}; server++ ))
do
  # call summarizer
  python "${BASE_DIR}"/exp_utils.py -s "${_dir[${server}]}" -r ${RUNS} 2>&1 >> ${EXPERIMENT_LOG[${server}]} &  
done


# The magic line
#   $$ holds the PID for this script
#   Negation means kill by process group id instead of PID
trap "kill -TERM -$$" SIGINT
wait
