import React, { useState } from 'react';
import { Box, Button, Input, FormControl, FormLabel, Heading } from '@chakra-ui/react';


const UserSearch = ({ fetchUserData }) => {
  const [username, setUsername] = useState(''); // State to store input value

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username) {
      fetchUserData(username); // Trigger a new API call
    }
  };

  return (
    <Box maxW="sm" borderWidth="1px" borderRadius="lg" p={4} m="auto" mt={'30%'}>
      <form onSubmit={handleSubmit}>
        <FormControl>
          <FormLabel htmlFor="username">Letterboxd Username</FormLabel>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)} // Update state as user types
            placeholder="Enter a username"
          />
          <Button type="submit" colorScheme="blue" ml={5}>Submit</Button>
        </FormControl>
      </form>
    </Box>
  );
};

export default UserSearch;