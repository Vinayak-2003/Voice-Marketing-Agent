// frontend/src/components/AgentForm.jsx
import React, { useState } from 'react';
import Input from './common/Input';
import Button from './common/Button';
import useAgentStore from '../store/agentStore';

const AgentForm = ({ onFormSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    system_prompt: '',
    voice_id: 'default_voice',
  });

  const createAgent = useAgentStore((state) => state.createAgent);
  const loading = useAgentStore((state) => state.loading);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createAgent(formData);
    setFormData({ name: '', system_prompt: '', voice_id: 'default_voice' }); // Reset form
    if (onFormSubmit) {
      onFormSubmit(); // Callback to close modal or refresh list
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <h2>Create New Agent</h2>
      <Input
        label="Agent Name"
        name="name"
        value={formData.name}
        onChange={handleChange}
        required
      />
      <div className="form-group">
        <label htmlFor="system_prompt">System Prompt</label>
        <textarea
          id="system_prompt"
          name="system_prompt"
          value={formData.system_prompt}
          onChange={handleChange}
          required
          rows="10"
          className="textarea"
          placeholder="You are a helpful AI assistant..."
        />
      </div>
      <Input
        label="Voice ID"
        name="voice_id"
        value={formData.voice_id}
        onChange={handleChange}
        required
      />
      <Button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create Agent'}
      </Button>
    </form>
  );
};

export default AgentForm;