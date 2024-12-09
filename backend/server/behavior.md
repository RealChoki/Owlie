1. get new thread
2. post new message
http://localhost:8000/api/threads/gAAAAABnVwvMrUHnaunGv8tsM5h5CTSifkPD0L0MHkHzOfx546ZWBW3Qmf3tIZrze347JAQYqMIAv4-ZuLMbeg-QLPEi_nbioI2eBfOqm0lgzgLnh5xxbnw=

{
    "content": "was ist java in 3 worten",
    "assistant_id": "gAAAAABnVwvLAPN3q5nxxytcoGJqUCUw8kp3K0ZzoNQjuRm2P2_1uAGeoMhttJBZV1mumKe6xic5CYrCU6p3K8lERAqESXNi3iUerjQvs8A0iVLlw7EsnvA="
}

receive:
{
    "run_id": "run_IGiT9Do3t5kLSVhu7EFFmFAj",
    "thread_id": "gAAAAABnVwyywz3XoEncWv0SWGlvHu9ZNsv1cD22nsYXjKSxf8ySv5oasKFzyQMhp7s7uCYg5YyvKDbh6KI4FzZ_NTTHB2QBnq_6pOBJhvR317rapGFpIso=",
    "status": "queued",
    "required_action": null,
    "last_error": null
}

3. wait and get information of the run:
http://localhost:8000/api/runs/gAAAAABnVwyywz3XoEncWv0SWGlvHu9ZNsv1cD22nsYXjKSxf8ySv5oasKFzyQMhp7s7uCYg5YyvKDbh6KI4FzZ_NTTHB2QBnq_6pOBJhvR317rapGFpIso=/run_IGiT9Do3t5kLSVhu7EFFmFAj

receive:
{
    "run_id": "run_IGiT9Do3t5kLSVhu7EFFmFAj",
    "thread_id": "thread_9fwl8WPTti77Tk1QxhLLvaRq",
    "status": "completed",
    "required_action": null,
    "last_error": null
}