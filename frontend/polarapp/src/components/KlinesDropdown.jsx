import React from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';

function KlinesDropdown({ onSelectKline, selectedKline }) {
  const klines = [
    { label: '1 MINUTE', value: '1m' },
    { label: '3 MINUTE', value: '3m' },
    { label: '5 MINUTE', value: '5m' },
    { label: '15 MINUTE', value: '15m' },
    { label: '30 MINUTE', value: '30m' },
    { label: '1 HOUR', value: '1h' },
    { label: '2 HOUR', value: '2h' },
    { label: '4 HOUR', value: '4h' },
    { label: '6 HOUR', value: '6h' },
    { label: '8 HOUR', value: '8h' },
    { label: '12 HOUR', value: '12h' },
    { label: '1 DAY', value: '1d' },
    { label: '3 DAY', value: '3d' },
    { label: '1 WEEK', value: '1w' },
    { label: '1 MONTH', value: '1M' }
  ];

  const handleKlineSelect = (eventKey, event) => {
    const selectedKline = klines.find(kline => kline.value === eventKey);
    onSelectKline(selectedKline.value);
  };
  

  return (
    <DropdownButton variant="outline-primary" id="dropdown-basic-button" title="Select Kline" onSelect={handleKlineSelect}>
      {klines.map((kline) => (
        <Dropdown.Item key={kline.value} eventKey={kline.value}>
          {kline.label}
        </Dropdown.Item>
      ))}
    </DropdownButton>
  );
}

export default KlinesDropdown;
