import React, { useState } from "react";
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";

// CSS Modules, react-datepicker-cssmodules.css
// import 'react-datepicker/dist/react-datepicker-cssmodules.css';

const DatePickers = () => {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());

  return (
    <>
    <DatePicker selected={startDate} onChange={(date) => setStartDate(date)} />
    <DatePicker selected={endDate} onChange={(date) => setEndDate(date)} />
    </>
  );
};

export default DatePickers;