import React, { useState } from "react";
import Message from "./Message";
import '../styles/ChatbotInterface.css';
import { backend_url } from '../config.js'

import IconButton from '@mui/material/IconButton';
import FileInput from "./FileInput";
// import SendIcon from '@mui/icons-material/Send';
import Button from '@mui/material/Button';
import Drawer from '@mui/material/Drawer';
import ArrowCircleUpIcon from '@mui/icons-material/ArrowCircleUp';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import CategoryOutlinedIcon from '@mui/icons-material/CategoryOutlined';
import BusinessIcon from '@mui/icons-material/Business';
import DownloadIcon from '@mui/icons-material/Download';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';

import axios from "axios";


function ChatbotInterface() {

    const [userMessage, setUserMessage] = useState([""]);
    // const [modelResponse, setModelResponse] = useState([""]);
    const [chatHistory, setChatHistory] = useState([]);
    const [selectedModel, setSelectedModel] = useState("gemini");
    const [open, setOpen] = useState(false);
    const [conversationTitle, setConversationTitle] = useState("")

    const toggleDrawer = (newOpen) => {
        setOpen(newOpen);
    }

    async function fetchData() {
        try {
            const getMessages = () => axios.get(`${backend_url}/${selectedModel}`, {
                params: { user_message: userMessage }
            });

            const [messages] = await Promise.all([getMessages()]);

            setChatHistory((prevHistory) => [
                ...prevHistory,
                { role: "model", model_rsp: messages.data.model || "There was a system error, please try again later!" }
            ]);

            setConversationTitle(messages.data.title)

        }
        catch (error) {
            console.error("Error fetching data: ", error);
        }

    }

    const handleModelChange = (e) => {
        setSelectedModel(e.target.value);
    }

    const handleKeyDown = (event) => {
        if (event.key === "Enter" && userMessage.trim() !== "") {
            handleSendMessage();
            event.preventDefault();
        }
    }

    const handleSendMessage = () => {

        if (userMessage.trim() !== "") {
            fetchData();
            setUserMessage("");
        } else {
            console.log("Type a message bro!");
        }

        setChatHistory((prevHistory) => [
            ...prevHistory,
            { role: "user", usr_msg: userMessage }
        ]);

    };

    return (
        <div className="wrapper">
            <div className="navbar">
                <button onClick={() => toggleDrawer(true)} className="button-svg">
                    <svg xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        className="svg-icon">
                        <rect width="18"
                            height="18" x="3" y="3" rx="2"></rect>
                        <path d="M9 3v18"></path>
                    </svg>
                </button>
                <h2>{conversationTitle}</h2>
                <Button sx={{
                    borderRadius: 3,
                    fontFamily: 'Roboto, sans-serif',
                    margin: 2.5,
                    backgroundColor: '#596ced',
                    fontWeight: 600
                }}
                    variant="contained">
                    Get Pro<sup>

                    </sup>
                </Button>
                <Drawer sx={{ width: 700 }} open={open} onClose={() => toggleDrawer(false)}>
                    <div className="drawer-container">
                        <div className="drawer-section1">
                            <Button className="button-menu" color="primary">
                                <AddCircleOutlineIcon sx={{ fill: '#ffffff', fontSize: 18 }} />
                                <span>New Chat</span>
                            </Button>
                            <Button className="button-menu" color="primary">
                                <CategoryOutlinedIcon sx={{ fill: '#ffffff', fontSize: 18 }} />
                                <span>Agents</span>
                            </Button>
                        </div>
                        <div className="drawer-section2">
                            <div className="drawer-section2-container">
                                <h4 className="drawer-section-title">Recent</h4>
                                <span className="history-conv-title">{conversationTitle}</span>
                            </div>
                        </div>
                        <div className="drawer-section3">
                            <Button className="button-menu" color="primary">
                                <BusinessIcon sx={{ fill: '#ffffff', fontSize: 18, marginRight: 1 }} />
                                <span>Business</span>
                            </Button>
                            <Button className="button-menu" color="primary">
                                <DownloadIcon sx={{ fill: '#ffffff', fontSize: 18, marginRight: 1 }} />
                                <span>Download</span>
                            </Button>
                            <Button className="button-menu" color="primary">
                                <MoreHorizIcon sx={{ fill: '#ffffff', fontSize: 18, marginRight: 1 }} />
                                <span>More</span>
                            </Button>
                        </div>
                        <div className="drawer-section4">
                            <div className="selectModel">
                                <label className="label" htmlFor="modelSelect"> Model: </label>
                                <select
                                    id="modelSelect"
                                    value={selectedModel}
                                    onChange={handleModelChange}>
                                    <option value="openai">OpenAi</option>
                                    <option value="gemini">Gemini</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </Drawer>
            </div >
            <div className="container">
                <div className="textbox-container">
                    <Message message={chatHistory} />
                </div>
            </div>
            <div className="wrapper-input-container">
                <div className="input-container">
                    <div className="wrapper-input-icon">
                        <input
                            className="insert-message"
                            type="text"
                            placeholder="Ask anything..."
                            value={userMessage}
                            onChange={(e) => setUserMessage(e.target.value)}
                            onKeyDown={handleKeyDown}></input>
                        <FileInput />
                        <IconButton color="primary" onClick={handleSendMessage}>
                            <ArrowCircleUpIcon
                                sx={{
                                    fill: userMessage === "" ? 'gray' : '#596ced',
                                    fontSize: 29
                                }}
                            />
                        </IconButton>
                    </div>
                </div>
            </div>
        </div >
    );
}

export default ChatbotInterface;