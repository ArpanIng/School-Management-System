const fetchCourses = async () => {
  try {
    const response = await fetch('/json/');
    data = response;
    console.log(data)
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

fetchCourses()