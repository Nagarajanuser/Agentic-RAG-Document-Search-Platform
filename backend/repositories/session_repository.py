from core.database import get_db_cursor


def save_chat_session(session_id: str, user_id: int):
    connection, cursor = get_db_cursor()

    cursor.execute(
        """
        INSERT INTO chat_sessions (
            session_id,
            user_id
        )
        VALUES (%s, %s)
        """,
        (session_id, user_id),
    )

    connection.commit()
    cursor.close()
    connection.close()


def save_chat_message(
    session_id: str,
    role: str,
    message: str,
):
    connection, cursor = get_db_cursor()

    cursor.execute(
        """
        INSERT INTO chat_messages (
            session_id,
            role,
            message
        )
        VALUES (%s, %s, %s)
        """,
        (
            session_id,
            role,
            message,
        ),
    )

    connection.commit()
    cursor.close()
    connection.close()


def get_chat_history(session_id: str, limit: int = 6):
    connection, cursor = get_db_cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM chat_messages
        WHERE session_id=%s
        ORDER BY message_id DESC
        LIMIT %s OFFSET 1
        """,
        (session_id, limit),
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    rows.reverse()

    history = []

    for role, message in rows:
        label = "User" if role == "user" else "Assistant"
        history.append(f"{label}: {message}")

    return "\n".join(history)
