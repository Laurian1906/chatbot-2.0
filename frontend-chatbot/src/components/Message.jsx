import React, { useEffect, useRef } from 'react';
import '../styles/Message.css';
import ReactMarkdown from "react-markdown";
import Box from '@mui/material/Box';

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
            {messageHistory.length > 0 ? messageHistory :
                <div className='placeholder-section' style={{ textAlign: "center" }}>
                    <p className='placeholder-text'>Don't know what to ask?</p>
                    <p className='placeholder-subtext'>Here are some suggestions</p>
                    <div className="question-box-container">
                        <Box className='question-box'>
                            <span className='box-text'>Do you like hiking?</span>
                        </Box>
                        <Box className='question-box'>
                            <span className='box-text'>Hi!</span>
                        </Box>
                        <Box className='question-box'>
                            <span className='box-text'>What is your favorite soap?</span>
                        </Box>
                        <Box className='question-box'>
                            <span className='box-text'>Cats are nice!</span>
                        </Box>
                    </div>

                </div>}
        </div>
    );
}

export default Message;
