import React, { useState, useEffect } from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import Form from 'react-bootstrap/Form';
import DropdownButton from 'react-bootstrap/DropdownButton';

const TOKEN_CSV_URL = '/tokens.csv';

const CustomMenu = React.forwardRef(({ children, style, className, 'aria-labelledby': labeledBy }, ref) => {
  const [value, setValue] = useState('');

  return (
    <div ref={ref} style={style} className={className} aria-labelledby={labeledBy}>
      <Form.Control
        autoFocus
        className="mx-3 my-2 w-auto"
        placeholder="Type to filter..."
        onChange={(e) => setValue(e.target.value)}
        value={value}
      />
      <ul className="list-unstyled" style={{ maxHeight: '200px', overflowY: 'scroll' }}>
        {React.Children.toArray(children).filter(
          (child) => !value || (child.props.children && child.props.children.toLowerCase().startsWith(value))
        )}
      </ul>
    </div>
  );
});

function TokenDropdown({onSelectToken, selectedToken, setSelectedToken}) {
  const [tokens, setTokens] = useState([]);

  useEffect(() => {
    async function fetchTokens() {
      const response = await fetch(TOKEN_CSV_URL);
      const csvData = await response.text();
      const lines = csvData.split('\n');
      const tokenList = lines.map((line) => {
        const [value, label] = line.split(',');
        return { value, label };
      });
      setTokens(tokenList);
    }
    fetchTokens();
  }, []);

  const handleTokenSelect = (eventKey, event) => {
    const selectedToken = event.target.innerText;
    setSelectedToken(selectedToken);
    onSelectToken(selectedToken);
  };

  return (
    <DropdownButton variant='outline-primary' id="dropdown-basic-button" title="Select Token" as="div" onSelect={handleTokenSelect}>
      <CustomMenu>
        {tokens.map((token) => (
          <Dropdown.Item key={token.value} eventKey={token.value}>
            {token.value}
          </Dropdown.Item>
        ))}
      </CustomMenu>
    </DropdownButton>
  );
}

export default TokenDropdown;
