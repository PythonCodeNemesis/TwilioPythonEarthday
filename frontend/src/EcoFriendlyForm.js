import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { responsivePropType } from "react-bootstrap/esm/createUtilityClasses";
import ecoimg from './ecoimg.jpg';

const SignUpForm = () => {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [frequency, setFrequency] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    console.log(
      JSON.stringify({
        phoneNumber: phoneNumber,
        frequency: frequency,
      })
    );

    var res;

    try {
      res = await fetch("http://127.0.0.1:5000/sign-up", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          phoneNumber: phoneNumber,
          frequency: frequency,
        }),
      });
    } catch (error) {
      console.log(error);
    }

    if (res.ok) {
      await res.json();
    } else {
      window.alert(res.status());
    }
  };

  return (
    <div style={containerStyle}>
      <img src={ecoimg} alt="this is car image" width={"400px"} height={"220px"}/>
      <h1 style={titleStyle}>Eco Friendly Reminder Service</h1>
      <Form onSubmit={handleSubmit} style={formStyle}>
        <Form.Group>
          <Form.Label style={formLabelStyle}>Phone Number</Form.Label>
          <Form.Control
            type="tel"
            value={phoneNumber}
            onChange={(event) => setPhoneNumber(event.target.value)}
            required
            style={formControlStyle}
          />
        </Form.Group>
        <Form.Group>
          <Form.Label style={formLabelStyle}>Frequency (hours)</Form.Label>
          <Form.Control
            type="number"
            value={frequency}
            onChange={(event) => setFrequency(event.target.value)}
            required
            style={formControlStyle}
          />
        </Form.Group>
        <Button type="submit" style={submitButtonStyle}>
          Sign Up
        </Button>
      </Form>
    </div>
  );
};

const containerStyle = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "50px",
  backgroundColor: "#7DCE82",
};

const imageStyle = {
  width: "150px",
  marginBottom: "25px",
};

const titleStyle = {
  marginBottom: "25px",
  color: "#FFFFFF",
};

const formStyle = {
  width: "50%",
  marginTop: "25px",
};

const formLabelStyle = {
  color: "#FFFFFF",
};

const formControlStyle = {
  backgroundColor: "#FFFFFF",
};

const submitButtonStyle = {
  backgroundColor: "#048C03",
  color: "#FFFFFF",
};



export default EcoFriendlyForm;
