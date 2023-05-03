import { ChangeEvent, FormEvent, useState } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';

const RegistrationForm = () => {
const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
});

const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
};

const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('Registration data:', formData);
};

return (
    <Container>
    <Row className="justify-content-md-center">
        <Col md="6">
        <h2>Register</h2>
        <Form onSubmit={handleSubmit}>
            <Row>
                <Col>
                <Form.Label>Username</Form.Label>
                </Col>
                <Col>
                <Form.Control
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                />
                </Col>
            </Row>
            <Row>
                <Col>
                <Form.Label>Email</Form.Label>
                </Col>
                <Col>
                <Form.Control
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />
                </Col>
            </Row>
            <Row>
                <Col>
                <Form.Label>Password</Form.Label>
                </Col>
                <Col>
                <Form.Control
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                />
                </Col>
            </Row>
            <Button variant="primary" type="submit">
                Register
            </Button>
        </Form>

        </Col>
    </Row>
    </Container>
);
};

export default RegistrationForm;
