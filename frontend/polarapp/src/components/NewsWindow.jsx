import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import { useState, useEffect } from "react";
import { Alert } from "react-bootstrap";



const ChatCard = ({ input_prompt }) => {
  
  const items = input_prompt.map((item, index) => (
    <Accordion.Item eventKey={index.toString()} key={index} >
      <Accordion.Header >{item.title}</Accordion.Header>
      <Accordion.Body>
        <p>Author: {item.author}</p>
        <p>Published at: {item.publishedAt}</p>
        <p>Source: {item.source.name}</p>
        <p>Description: {item.description}</p>
        <p>Content: {item.content}</p>
        <Button
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          variant="outline-primary"
        >
          Source Link
        </Button>
      </Accordion.Body>
    </Accordion.Item>
  ));

  return (
      <Accordion >{items}</Accordion>

  );
};


let BASE_URL = "http://localhost:8001/api/v1/news"
function NewsWindow() {



    const [prompt, setPrompt] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
        try {
            const response = await fetch(`${BASE_URL}/?symbol=BTC`);
            if (!response.ok) {
            throw new Error("Error fetching prompts");
            }
            const json = await response.json();
            setPrompt(json);
        } catch (error) {
            console.error(error);
            setError("Error connecting to database from NewsWindow");
        }
        };
        
        fetchData();
    }, []);


  return (
    
    <Card.Body>
      {prompt && Array.isArray(prompt) && prompt.length > 0 ? (
        prompt.map((el, index) => (
          <ChatCard key={index} prompt={el} />
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

export default NewsWindow;