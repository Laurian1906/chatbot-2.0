import React, { useEffect, useRef } from 'react';
import '../styles/Message.css';
import ReactMarkdown from "react-markdown";

function Message({ message }) {
    const lastMessageRef = useRef(null);

    useEffect(() => {
        if (lastMessageRef.current) {
            lastMessageRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [message]);

    let messageHistory = [];

    for (let j = 0; j < message.length; j++) {
        const isLastMessage =
            (j === message.length - 1 && (message[j].role === "model" || message[j].role === "user"));

        messageHistory.push(
            <div
                key={j}
                ref={isLastMessage ? lastMessageRef : null}
                className={message[j].role === "user" ? "message-user" : "message-ai"}
            >
                {message[j].role === "model" ? (
                    // Afișează răspunsul modelului cu Markdown
                    <ReactMarkdown>{message[j].model_rsp}</ReactMarkdown>
                ) : (
                    // Mesajul utilizatorului afișat simplu
                    <span>{message[j].usr_msg}</span>
                )}
            </div>
        );
    }

    return (
        <div className='messageBox'>
            {messageHistory.length > 0 ? messageHistory : <div className='placeholder-text' style={{ textAlign: "center" }}>What will you tackle today?</div>}
        </div>
    );
}

export default Message;
