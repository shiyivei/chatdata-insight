import { useState, useEffect } from "react";
import { Card, Alert, Toast } from "react-bootstrap";

const ChatCard = ({input_prompt}) => { 
  
  let {prompt, completion, createdAt} = input_prompt
  
  return (
    
    
    <Toast className="toast" >
        <Toast.Header toaster-options="{'close-button':false}">
            <strong className="me-auto">{prompt}</strong>
            <small>{createdAt}</small>
        </Toast.Header>
        <Toast.Body>{completion}</Toast.Body>
    </Toast>

)
}

let BASE_URL = "http://localhost:8001/api/v1/openai"

function ChatList() {
    const [prompt, setPrompt] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
        try {
            const response = await fetch(`${BASE_URL}`);
            if (!response.ok) {
            throw new Error("Error fetching prompts");
            }
            const json = await response.json();
            setPrompt(json);
        } catch (error) {
            console.error(error);
            setError("Error connecting to database");
        }
        };
        
        fetchData();
    }, []);

  return (
      <Card.Body>
        {prompt && prompt.length > 0 ? (
        prompt.map((el) => (
            <ChatCard key={el._id} input_prompt={el} />
        ))
        ) : error ? (
        <Alert key={"danger"} variant={"danger"}>
            {error}
        </Alert>
        ) : (
        <Alert key={"primary"} variant={"primary"}>
            Database empty on Prompts
        </Alert>
        )}
      </Card.Body>
    );
}

export default ChatList;
