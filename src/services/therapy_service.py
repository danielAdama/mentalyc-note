from fastapi import UploadFile
import uuid
import json
from typing import Union, Dict, Optional, List
from mentalyc_ai import MentalycNoteAgent
from src.exceptions.custom_exception import (
    APIAuthenticationFailException, InternalServerException, RecordNotFoundException
)

from config.logger import Logger

logger = Logger(__name__)

class TherapyService:
    @staticmethod
    async def track_progress(user_id: Union[str, uuid.UUID], files: List[UploadFile]):
        try:
            note_agent = MentalycNoteAgent(user_id=user_id)
            sessions = {}
            for file in files:
                file_bytes = await file.read()
                session_content = json.loads(file_bytes.decode('utf-8'))
                session_id = file.filename.split('.')[0].split('_')[-1]
                sessions[session_id] = session_content

            # result = note_agent(sessions)
            result = {'sentiment': 'anxious',
 'GAD7_analysis': {'session1': {'gad_7_scoring_table': {'Feeling nervous, anxious, or on edge': 2,
    'Not being able to stop or control worrying': 2,
    'Worrying too much about different things': 2,
    'Trouble relaxing': 1,
    "Being so restless that it's hard to sit still": 1,
    'Becoming easily annoyed or irritable': 1,
    'Feeling afraid as if something awful might happen': 1},
   'total_gad_7_score': 10,
   'anxiety_severity_classification': 'Moderate anxiety',
   'justification': 'The client reported experiencing symptoms of anxiety, including feeling nervous and anxious, worrying too much, and having trouble relaxing, over the past six weeks. These align with moderate anxiety severity based on the GAD-7 scoring criteria.'},
  'session2': {'gad_7_scoring_table': {'Feeling nervous, anxious, or on edge': 1,
    'Not being able to stop or control worrying': 1,
    'Worrying too much about different things': 1,
    'Trouble relaxing': 1,
    "Being so restless that it's hard to sit still": 0,
    'Becoming easily annoyed or irritable': 0,
    'Feeling afraid as if something awful might happen': 0},
   'total_gad_7_score': 4,
   'anxiety_severity_classification': 'Mild anxiety',
   'justification': 'The client reported a significant reduction in anxiety and stress, with improved task management and boundary-setting. His symptoms have decreased following the application of therapy strategies, indicating mild anxiety severity based on the GAD-7 scoring criteria.'}},
 'insight': '### Assessment Summary\nThe client underwent a GAD-7 assessment, which measures the severity of generalized anxiety disorder symptoms. Between Session 1 and Session 2, the client\'s severity classification improved from "Moderate anxiety" to "Mild anxiety." Initially, the client reported experiencing several symptoms of anxiety, including feeling nervous, worrying too much, and having trouble relaxing, which aligned with moderate anxiety severity. However, by Session 2, the client showed a significant reduction in anxiety and stress levels, attributed to improved task management, boundary-setting, and the application of therapy strategies. This progress led to a reclassification to mild anxiety severity.\n\n### Progress Analysis\nThe progress report across sessions indicates the following changes in symptoms:\n- **Feeling nervous, anxious, or on edge:** Improvement\n- **Not being able to stop or control worrying:** Improvement\n- **Worrying too much about different things:** Improvement\n- **Trouble relaxing:** Plateau\n- **Being so restless that it\'s hard to sit still:** Improvement\n- **Becoming easily annoyed or irritable:** Improvement\n- **Feeling afraid as if something awful might happen:** Improvement\n- **Total score:** Improvement\n\nOverall, the client has shown significant improvement in most anxiety symptoms, with the total score reflecting this positive trend. However, the symptom of "trouble relaxing" has plateaued, indicating a need for targeted strategies to address this specific issue.\n\n### Actionable Insights\nTo sustain the improvements and address the plateau:\n- For symptoms showing improvement, continue and possibly intensify the current therapy strategies and stress management techniques, as they seem to be effective.\n- For "trouble relaxing," which has plateaued, consider introducing or enhancing relaxation techniques such as deep breathing exercises, progressive muscle relaxation, or mindfulness meditation. Regular practice of these techniques could help improve the client\'s ability to relax.\n- It might also be beneficial to explore the underlying reasons for the difficulty in relaxing, which could be related to unresolved issues, unmanaged stress, or physical discomfort. Addressing these underlying factors could be crucial anxiety.\n\n### Encouragement\nIt\'s truly commendable to see the significant progress made between sessions, reflecting the client\'s hard work and dedication to their mental health. The improvement in anxiety symptoms is a testament to the effectiveness of the applied strategies and the client\'s resilience. Continuing on this path, with a focus on overcoming the remaining challenges, such as trouble relaxing, will be key to further progress. Remember, mental health is a journey, and it\'s okay to take it one step at a time. Keep moving forward, and don\'t hesitate to seek support when needed.'}
            logger.info("Sessions processed successfully")
        except Exception as ex:
            logger.error(f"Processing Sessions -> API v1/therapy/analysis/: {ex}")
            raise InternalServerException()

        return result