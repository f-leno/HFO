#!/bin/bash

echo "[$(date +"%Y-%m-%d_%H:%M:%S")] RUNNING HFO EXPERIMENT"

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
  OFFENSE_AGENTS=2
fi
if [ -z "${DEFENSE_AGENTS+x}" ]; then
  DEFENSE_AGENTS=0
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

#Now the number of trials is incremented to take into account how many
# evaluation trials will be carried out
((EVAL_COUNT=${TRIALS}/${INTERVAL}))
((EVAL_TRIALS=${EVAL_COUNT}*${DURATION}))
((TRIALS_TOTAL=${TRIALS}+${EVAL_TRIALS}))


BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

for ((server=0; server<${PARALLEL_SERVER}; server++ ))
do
  _now=$(date +"%Y_%m_%d-%H.%M.%S")
  _dir[${server}]="${BASE_DIR}/LOGS/${_now}_${AGENT}/"
  mkdir -p ${_dir[${server}]};

  EXPERIMENT_LOG[${server}]="${_dir[${server}]}EXPERIMENT_LOG"
  touch "${EXPERIMENT_LOG[${server}]}"
  echo "[$(date +"%Y-%m-%d_%H:%M:%S")] START EXPERIMENT" >> ${EXPERIMENT_LOG[${server}]}
  echo "=====================================" >> ${EXPERIMENT_LOG[${server}]}
  echo \
  "./experiments/run.sh\
    --runs=${RUNS} --trials=${TRIALS}\
    --max-frames-per-trial=${MAX_FRAMES}\
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

killall -9 rcssserver


for ((run=1; run<=${RUNS}; run++ ))
do
  alive_server=0
  alive_agents=0
  for ((server=0; server<${PARALLEL_SERVER}; server++ ))
  do
    ((alive_server++))
    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] STARTING RUN ${run} ==================" >> ${EXPERIMENT_LOG[${server}]}
    sleep 2
    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] STARTING HFO SERVER" >> ${EXPERIMENT_LOG[${server}]}
    ((HFO_PORT[${server}]=${PORT}+50*${server}))
    SERVER_LOG="${_dir[${server}]}SERVER_LOG_${run}_${server}"
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
    --seed ${SEED}\
    ${MODE}\
    --fullstate >> ${SERVER_LOG} &" >> ${SERVER_LOG}
    echo "=====================================" >> ${SERVER_LOG}

    ./bin/HFO \
    --port "${HFO_PORT[${server}]}" \
    --log-dir "${_dir[${server}]}" \
    --offense-agents "${OFFENSE_AGENTS}" \
    --defense-npcs "${DEFENSE_AGENTS}" \
    --trials "${TRIALS_TOTAL}" \
    --frames-per-trial "${MAX_FRAMES}" \
    --seed "${SEED}" \
    "${MODE}" \
    --fullstate >> ${SERVER_LOG} &
    # maybe add:
    #--ball-x-min 0.4 \
    #--ball-x-max 0.5 \
    # instead of headless: --no-sync \
    HFO_PID[${server}]=$!
    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] HFO SERVER PID: ${HFO_PID[${server}]}" >> ${EXPERIMENT_LOG[${server}]}

    echo "[$(date +"%Y-%m-%d_%H:%M:%S")] ${alive_server} SERVER SHOULD BE RUNNING NOW"

    for ((agent=1; agent<=${OFFENSE_AGENTS}; agent++ ))
    do
      ((alive_agents++))
      AGENT_LOG="${_dir[${server}]}AGENT_LOG_${run}_${agent}"
      touch "${AGENT_LOG}"
      sleep 2
      echo "[$(date +"%Y-%m-%d_%H:%M:%S")] STARTING AGENT ${agent}" >> ${EXPERIMENT_LOG[${server}]}
      echo "[$(date +"%Y-%m-%d_%H:%M:%S")] STARTING AGENT ${agent}" >> ${AGENT_LOG}
      echo "=====================================" >> ${AGENT_LOG}
      echo \
      "${BASE_DIR}/experiment.py -p ${HFO_PORT[${server}]} -a ${AGENT} -i ${INTERVAL} -d\
      ${DURATION} -t ${TRIALS} -l ${_dir[${server}]}${AGENT}_${run} -s ${SEED}\
      >> ${AGENT_LOG} & >> ${AGENT_LOG}" >> ${EXPERIMENT_LOG[${server}]}
      echo "=====================================" >> ${AGENT_LOG}
      "${BASE_DIR}"/experiment.py -p "${HFO_PORT[${server}]}" -a "${AGENT}" -i "${INTERVAL}" -d \
      "${DURATION}" -t "${TRIALS}" -l "${_dir[${server}]}${AGENT}"_"${run}" -s "${SEED}"\
      >> ${AGENT_LOG} &

      echo "[$(date +"%Y-%m-%d_%H:%M:%S")] ${alive_agents} AGENTS SHOULD BE RUNNING NOW"
    done

  done

  for ((server=0; server<${PARALLEL_SERVER}; server++ ))
  do
    wait ${HFO_PID[${server}]}
    sleep 2
    #kill -9 rcssserver  >> ${EXPERIMENT_LOG}
    mv -v "${_dir[${server}]}"incomplete.hfo "${_dir[${server}]}"incomplete_"${run}".hfo >> ${EXPERIMENT_LOG[${server}]}
  done                                                               

done

# The magic line
#   $$ holds the PID for this script
#   Negation means kill by process group id instead of PID
trap "kill -TERM -$$" SIGINT
wait
