export const fetchUserData = async (username) => {
    try {
      const response = await fetch(`http://localhost:5000/allfilms/${username}`);
      const data = await response.json();
      console.log(data)
      return data;
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
};