from fastapi import APIRouter
import os
from pathlib import Path

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/env", summary="Check environment variables", operation_id="check_environment")
async def check_environment():
    """
    Debug endpoint to check environment variables and system info.
    """
    return {
        "environment_variables": {
            "SENDGRID_API_KEY": "set" if os.environ.get('SENDGRID_API_KEY') else "missing",
            "NOTIFICATION_EMAIL": "set" if os.environ.get('NOTIFICATION_EMAIL') else "missing",
        },
        "paths": {
            "current_dir": str(Path.cwd()),
            "file_dir": str(Path(__file__).parent),
            "data_dir": str(Path(__file__).parent.parent.parent / "data"),
            "questions_file": str(Path(__file__).parent.parent.parent / "data" / "questions.json"),
        },
        "file_system": {
            "data_dir_exists": (Path(__file__).parent.parent.parent / "data").exists(),
            "questions_file_exists": (Path(__file__).parent.parent.parent / "data" / "questions.json").exists(),
            "data_dir_writable": os.access(str(Path(__file__).parent.parent.parent / "data"), os.W_OK) if (Path(__file__).parent.parent.parent / "data").exists() else False,
        }
    }


@router.get("/file-contents", summary="Check questions file contents", operation_id="check_file_contents")
async def check_file_contents():
    """
    Debug endpoint to check the contents of the questions file.
    """
    import json
    
    questions_file = Path(__file__).parent.parent.parent / "data" / "questions.json"
    
    result = {
        "file_path": str(questions_file),
        "file_exists": questions_file.exists(),
        "questions": [],
        "error": None
    }
    
    if questions_file.exists():
        try:
            with open(questions_file, 'r', encoding='utf-8') as f:
                questions = json.load(f)
                result["questions"] = questions
                result["total_count"] = len(questions)
        except Exception as e:
            result["error"] = str(e)
    
    return result


@router.post("/test-email", summary="Test email sending", operation_id="test_email_sending")
async def test_email_sending():
    """
    Debug endpoint to test email sending functionality.
    """
    from app.services import send_question_notification
    
    test_question_data = {
        "id": "test_email_123",
        "talk_id": "test-talk",
        "name": "Test Email User",
        "email": "test@example.com",
        "question": "This is a test email to verify email functionality is working.",
        "submitted_at": "2026-01-06T15:00:00.000000"
    }
    
    try:
        send_question_notification(test_question_data)
        return {
            "success": True,
            "message": "Email test triggered, check server logs for details"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Email test failed"
        }