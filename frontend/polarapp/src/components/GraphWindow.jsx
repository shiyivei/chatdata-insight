import React, { useEffect, useState } from 'react';
import Plotly from 'plotly.js-dist';
import Spinner from 'react-bootstrap/Spinner';
import { ButtonGroup } from 'react-bootstrap';
import TokenDropdown from './TokenDropdown';
import DatePickers from './DatePickers';
import KlinesDropdown from './KlinesDropdown';

let BASE_URL = 'http://127.0.0.1:8001/api/v1/binance';

const GraphWindow = () => {
  const [myData, setMyData] = useState([]);
  const [dateRange, setDateRange] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedToken, setSelectedToken] = useState('BTC');
  const [selectedKline, setSelectedKline] = useState('15m');

  const handleSelectToken = (token) => {
    setSelectedToken(token);
    setIsLoading(true); // Set isLoading to true when token is changed
  };

  const handleSelectKline = (klines) => {
    setSelectedKline(klines);
    setIsLoading(true); // Set isLoading to true when kline is changed
  };
  
  
  useEffect(() => {
    if (selectedToken && selectedKline) { // Make sure there is a selected token before making the fetch request
      setIsLoading(true); // Set isLoading to true before making the fetch request
      fetch(`${BASE_URL}/?symbol=${selectedToken}&currency=USDT&klines=${selectedKline}&dataframe=["2023-05-06", "2023-05-06"]`)
        .then(response => response.json())
        .then(data => {
          const trace1 = {
            x: data.map(d => d.open_timestamp),
            close: data.map(d => d.close),
            decreasing: { line: { color: 'rgba(255,50,10,1)' } },
            high: data.map(d => d.high),
            increasing: { line: { color: 'rgba(31,119,180,1)' } },
            line: { color: 'rgba(31,119,180,1)' },
            low: data.map(d => d.low),
            open: data.map(d => d.open),
            type: 'candlestick',
            xaxis: 'x',
            yaxis: 'y'
          };
          setMyData([trace1]);
          const dates = data.map(d => d.date);
          const range = [dates[0], dates[dates.length - 1]];
          setDateRange(range);
          setIsLoading(false);
        })
        .catch(error => console.error(error));
    }
  }, [selectedToken, selectedKline]);

  useEffect(() => {
    if (!isLoading) {
      const layout = {
        dragmode: 'zoom',
        margin: {
          r: 10,
          t: 25,
          b: 40,
          l: 60
        },
        showlegend: false,
        xaxis: {
          autorange: true,
          rangeslider: { range: dateRange },
          title: "TimeStamp",
          type: 'date'
        },
        yaxis: {
          autorange: true,
          type: 'linear'
        },
      };
      Plotly.newPlot('myDiv', myData, layout);
    }
  }, [myData, dateRange, isLoading]);

  return (
    <div>
      <ButtonGroup className='chat-window-menu'>
        <TokenDropdown className='menu-item' onSelectToken={handleSelectToken} selectedToken={selectedToken} setSelectedToken={setSelectedToken} />
        <KlinesDropdown className='menu-item' onSelectKline={handleSelectKline} selectedKline={selectedKline} setSelectedKline={setSelectedKline} />
        <p>{selectedToken}</p>
        <DatePickers />
      </ButtonGroup>
  
      {isLoading && (
        <div className="spinner-container">
          <Spinner animation="border" variant="primary" />
        </div>
      )}
  
      {!isLoading && (
        <div id="myDiv"></div>
      )}
    </div>
  );
  
  
};

export default GraphWindow;
