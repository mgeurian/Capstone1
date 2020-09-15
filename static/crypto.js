const BASE_URL = `http://127.0.0.1:5000`

async function processForm(e) {
  e.preventDefault()

  // data collection for api

  let name = $('#name').val();

  const res = await axios.post(`http://127.0.0.1:5000/api/cryptodata`, { name });


  

  let cryptoData =$(handleResponse(res));
    $('#currency-list').append(cryptoData)
}

function handleResponse(res) {


  return `
    <div>
      <p>Your id for ${res.data.data[1].name} is ${res.data.data[1].id}.</p>
    </div>
  `; 

}

$("#crypto-form").on("submit", processForm);