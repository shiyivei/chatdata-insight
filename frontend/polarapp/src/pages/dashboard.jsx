import Container from "react-bootstrap/Container";
import Card from 'react-bootstrap/Card';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import Menu from "../components/Navbar"
import GraphWindow from '../components/GraphWindow'
import ChatList from '../components/ChatHistory'

import React, { useState, useEffect } from 'react';
import axios from 'axios';


const Dashboard = () => {

  let BASE_URL = "http://localhost:8001/api/v1/openai"

  const [inputValue, setInputValue] = useState('');
  const [error, setError] = useState(null);
  const [prompt, setPrompt] = useState([]);
  const [postingPrompt, setPostingPrompt] = useState(false); // added state for tracking if prompt is being posted
  

  useEffect(() => {
    let timeout;
    if (error) {
      timeout = setTimeout(() => {
        setError(null);
      }, 3000);
    }
    return () => clearTimeout(timeout);
  }, [error]);
  

  const handleSubmit = async (event) => { 
    event.preventDefault();
    
    if (!inputValue.trim()) {
      setError("Please enter a prompt");
      return;
    }
  
    setPostingPrompt(true); // set postingPrompt to true before making POST request
  
    try {
      const response = await axios({
        method: 'POST',
        url: `${BASE_URL}`,
        data: JSON.stringify({"prompt": inputValue}),
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
      });
  
      const newPrompt = await response.data;
      setPrompt([...prompt, newPrompt]);
      setInputValue("");
    } catch (error) {
      console.error(error);
      setError("Could not connect to server from Dashboard");
    } finally {
      setPostingPrompt(false); // set postingPrompt to false after POST request is completed
    }
  };
  
  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };
  

    return (
        <Container fluid='True' >
              
            <Menu />

            <Container className="mw-100">

                <Row className="">

                    <Col xs={12} md={8} className="gx-4">

                      <Row>
                        
                        <Card className="gy-1 graphwindow overflow-auto">

                          <Card.Body>

                              <GraphWindow />

                          </Card.Body>
                        </Card>
                      </Row>

                      <Row>
                      <Card className="gy-1 newswindow overflow-auto">
                          <Card.Body>
                            

                          </Card.Body>
                        </Card>
                      </Row>

                    </Col>


                    <Col xs={12} md={4} className="gx-2">
                    
                    <Card className="chatwindow overflow-auto">
                      {postingPrompt ? (
                        <div className="spinner-container">
                          <Spinner animation="border" variant="primary" />
                        </div>
                      ) : (
                        <ChatList />
                      )}
                      {error && (
                        <Alert className="fade-out" variant="danger">
                          {error}
                        </Alert>
                      )}
                    </Card>

                      <Card>
                        <Card.Footer className="text-muted chatinput">
                        

                        <Form onSubmit={handleSubmit} className="">
                          <InputGroup className="mb-3 chatinput">
                            <Form.Control
                              type="text"
                              placeholder="Show me the price of bitcoin in USD"
                              aria-label="prompt-input"
                              value={inputValue}
                              onChange={handleInputChange}
                            />
                            <Button variant="outline-dark" type="submit" >Submit</Button>
                          </InputGroup>
                        </Form>

                        </Card.Footer>
                      </Card>
                    </Col>

                </Row>
            </Container>

        </Container>

    )

    
}
export default Dashboard
