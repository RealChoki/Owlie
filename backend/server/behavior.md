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

### Moodle
1. send moodle related question:
http://localhost:8000/api/threads/gAAAAABnVwvMrUHnaunGv8tsM5h5CTSifkPD0L0MHkHzOfx546ZWBW3Qmf3tIZrze347JAQYqMIAv4-ZuLMbeg-QLPEi_nbioI2eBfOqm0lgzgLnh5xxbnw=
{
    "content": "was sind die termine für diesen kurs",
    "assistant_id": "gAAAAABnVwvLAPN3q5nxxytcoGJqUCUw8kp3K0ZzoNQjuRm2P2_1uAGeoMhttJBZV1mumKe6xic5CYrCU6p3K8lERAqESXNi3iUerjQvs8A0iVLlw7EsnvA="
}

receive:
{
    "run_id": "run_EGjBZmUsNTxd3Pmbn0szjYRG",
    "thread_id": "gAAAAABnV0O46Aqazfv6VnmsiP9lNob7XXOM7BHmfuivEH1nNzZUm9rbUNuozpABGlWvr5BOk6j5DLWvuNYk2A8NvV06_CJYQAjotW4XQo8dqd0jk74hqXQ=",
    "status": "queued",
    "required_action": null,
    "last_error": null
}

2. get info of the run:
http://localhost:8000/api/runs/gAAAAABnVwyywz3XoEncWv0SWGlvHu9ZNsv1cD22nsYXjKSxf8ySv5oasKFzyQMhp7s7uCYg5YyvKDbh6KI4FzZ_NTTHB2QBnq_6pOBJhvR317rapGFpIso=/run_EGjBZmUsNTxd3Pmbn0szjYRG

receive:
{
    "run_id": "run_EGjBZmUsNTxd3Pmbn0szjYRG",
    "thread_id": "thread_9fwl8WPTti77Tk1QxhLLvaRq",
    "status": "requires_action",
    "required_action": {
        "submit_tool_outputs": {
            "tool_calls": [
                {
                    "id": "call_AQLMNRSuu61t8OsfNcCP4ORc",
                    "function": {
                        "arguments": "{\"courseid\":\"51589\"}",
                        "name": "get_moodle_course_content"
                    },
                    "type": "function"
                }
            ]
        },
        "type": "submit_tool_outputs"
    },
    "last_error": null
}

### run
1. run object
Run(
    id='run_1cOfWuh0hv4MuTgPwZ4OB5v9',
    assistant_id='asst_ITEK83NLc8Uigo2jTka6nUOt',
    cancelled_at=None,
    completed_at=None,
    created_at=1733777005,
    expires_at=1733777605,
    failed_at=None,
    incomplete_details=None,
    instructions=(long text from choki),
    last_error=None,
    max_completion_tokens=None,
    max_prompt_tokens=None,
    metadata={},
    model='gpt-4o-mini',
    object='thread.run',
    parallel_tool_calls=True,
    required_action=None,
    response_format='auto',
    started_at=None,
    status='queued',
    thread_id='thread_iHd8axtuiLTow8JfZP7uQKm2',
    tool_choice='auto',
    tools=[
        FunctionTool(
            function=FunctionDefinition(
                name='get_moodle_course_content',
                description='Fetches Moodle course content based on course ID.',
                parameters={
                    'type': 'object',
                    'required': ['courseid'],
                    'properties': {
                        'courseid': {'type': 'string', 'description': "The Moodle course ID, e.g., '51589'."}
                    }
                },
                strict=False
            ),
            type='function'
        ),
        FileSearchTool(
            type='file_search',
            file_search=FileSearch(
                max_num_results=None,
                ranking_options=FileSearchRankingOptions(
                    score_threshold=0.0,
                    ranker='default_2024_08_21'
                )
            )
        )
    ],
    truncation_strategy=TruncationStrategy(
        type='auto',
        last_messages=None
    ),
    usage=None,
    temperature=1.0,
    top_p=1.0,
    tool_resources={}
)

2. moodle related run
Run(
    id='run_1cOfWuh0hv4MuTgPwZ4OB5v9',
    assistant_id='asst_ITEK83NLc8Uigo2jTka6nUOt',
    cancelled_at=None,
    completed_at=None,
    created_at=1733777005,
    expires_at=1733777605,
    failed_at=None,
    incomplete_details=None,
    instructions=(),
    last_error=None,
    max_completion_tokens=None,
    max_prompt_tokens=None,
    metadata={},
    model='gpt-4o-mini',
    object='thread.run',
    parallel_tool_calls=True,
    required_action=RequiredAction(
        submit_tool_outputs=RequiredActionSubmitToolOutputs(
            tool_calls=[
                RequiredActionFunctionToolCall(
                    id='call_VQzx7OcEtT3zviyQmlS7HR40',
                    function=Function(
                        arguments='{"courseid":"51589"}',
                        name='get_moodle_course_content'
                    ),
                    type='function'
                )
            ]
        ),
        type='submit_tool_outputs'
    ),
    response_format='auto',
    started_at=1733777005,
    status='requires_action',
    thread_id='thread_iHd8axtuiLTow8JfZP7uQKm2',
    tool_choice='auto',
    tools=[
        FunctionTool(
            function=FunctionDefinition(
                name='get_moodle_course_content',
                description='Fetches Moodle course content based on course ID.',
                parameters={
                    'type': 'object',
                    'required': ['courseid'],
                    'properties': {
                        'courseid': {
                            'type': 'string',
                            'description': "The Moodle course ID, e.g., '51589'."
                        }
                    }
                },
                strict=False
            ),
            type='function'
        ),
        FileSearchTool(
            type='file_search',
            file_search=FileSearch(
                max_num_results=None,
                ranking_options=FileSearchRankingOptions(
                    score_threshold=0.0,
                    ranker='default_2024_08_21'
                )
            )
        )
    ],
    truncation_strategy=TruncationStrategy(
        type='auto',
        last_messages=None
    ),
    usage=None,
    temperature=1.0,
    top_p=1.0,
    tool_resources={}
)



1. moodle related question for course "51589":
http://localhost:8000/api/threads/gAAAAABnV2pyPugOwn-UYKtoBS-pPnhZXP3A_8mb8dpU8Cujm4_tuzQkCD8EyUpcjWIYnEH9SxsS_r3NtxcNzHPOA4Ptep5eR10g3au1ZVxKaBWEyW_JhnU=

{
    "content": "gib mir die termine von moodle",
    "assistant_id": "gAAAAABnVwvLAPN3q5nxxytcoGJqUCUw8kp3K0ZzoNQjuRm2P2_1uAGeoMhttJBZV1mumKe6xic5CYrCU6p3K8lERAqESXNi3iUerjQvs8A0iVLlw7EsnvA="
}

receive:
http://localhost:8000/api/threads/gAAAAABnV2pyPugOwn-UYKtoBS-pPnhZXP3A_8mb8dpU8Cujm4_tuzQkCD8EyUpcjWIYnEH9SxsS_r3NtxcNzHPOA4Ptep5eR10g3au1ZVxKaBWEyW_JhnU=
{
    "content": "Hier sind die Termine, die für den Kurs zur Tutor*innenqualifizierung festgelegt wurden:\n\n- **25.10.**: 09-15 Uhr, WH Gebäude C 406\n- **26.10.**: 10-15 Uhr, WH Gebäude C 406\n- **08.11.**: 09-12 Uhr, online in Zoom: [Zoom-Link](https://htw-berlin.zoom-x.de/j/69859765876) (+Aufgabe mit flexibler Zeiteinteilung)\n- **22.11.**: 09-14 Uhr, WH Gebäude C 406\n\nFalls du noch weitere Informationen benötigst, zögere nicht, nachzufragen!",
    "role": "assistant",
    "hidden": false,
    "id": "msg_gE1YxTsb20nPXgCXLhc4AjiA",
    "created_at": 1733782144
},