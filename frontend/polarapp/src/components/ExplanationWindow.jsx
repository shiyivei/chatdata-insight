// import two hooks from react
import { useState, useEffect } from 'react'
import { Alert } from 'react-bootstrap'

let BASE_URL = "http://localhost:8001/api/v1/openai"


const ChatCard = ({input_prompt}) => { 

    let {prompt} = input_prompt

    return (

      <div className="chathistory">
          
          <Alert className='explanation-prompt-badge' >
          <b>Explanation:</b> <br />
          {prompt}
          </Alert>

        
       
      </div>
  )
}

const PromptExplanationWindow = () => {

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
          setError("Error connecting to database from ExplanationWindow");
        }
      };
      
      fetchData();
    }, []);

    
    return (

      <div> 
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
      </div>
          

    )

    
}
export default PromptExplanationWindow
