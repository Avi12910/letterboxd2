import { useState, useEffect } from 'react';
import { fetchUserData } from '../utils/api';

const useUserData = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getData = async () => {
      const userData = await fetchUserData();
      setData(userData);
      setLoading(false);
    };
    getData();
  }, []);

  return { data, loading };
};

export default useUserData;