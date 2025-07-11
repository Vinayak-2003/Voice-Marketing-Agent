// frontend/src/components/common/Input.jsx
import React from 'react';

const Input = ({ label, name, value, onChange, type = 'text', required = false }) => {
  return (
    <div className="form-group">
      <label htmlFor={name}>{label}</label>
      <input
        type={type}
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        className="input"
      />
    </div>
  );
};

export default Input;