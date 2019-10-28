
function register_begin(resident_key=false){
  fetch('/register/options', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({'resident_key': resident_key})
  }).then(function(response) {
    if(response.ok) return response.arrayBuffer();
  }).then(CBOR.decode).then(function(options) {
    console.log("register options:");
    console.log(JSON.stringify(options));
    return navigator.credentials.create(options);
  }).then(function(attestation) {
    attestationObject = CBOR.decode(attestation.response.attestationObject);
    console.log(JSON.stringify(attestationObject, "\t"));
    authData = attestationObject.authData
    console.log(authData);
    return fetch('/register/response', {
      method: 'POST',
      headers: {'Content-Type': 'application/cbor'},
      body: CBOR.encode({
        "attestationObject": new Uint8Array(attestation.response.attestationObject),
        "clientDataJSON": new Uint8Array(attestation.response.clientDataJSON),
      })
    });
  }).then(function(response) {
    if (response.ok) {
      console.log('Registration succeeded.');
      location.reload();
    } else {
      alert('Registration failed.');
    }
  }, function(reason) {
    alert(reason);
  });
}

function remove_credential(credential_id){
  console.log("credential_id: " + credential_id);
  fetch('/remove_credential', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({'credential_id': credential_id})
  }).then(function(response) {
    if (response.ok) {
      window.location = '/home';
    } else {
      alert('remove failed.');
    }
  });
}

function login_fido2(username){
  let body = '{}';
  if (username != null) {
    body = JSON.stringify({'username': username});
  }
  fetch('/assertion/options', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: body
  }).then(function(response) {
    if(response.ok) return response.arrayBuffer();
    throw new Error('No credential available to authenticate!');
  }).then(CBOR.decode).then(function(options) {
    console.log(JSON.stringify(options));
    return navigator.credentials.get(options);
  }).then(function(assertion) {
    console.log(assertion)
    return fetch('/assertion/response', {
      method: 'POST',
      headers: {'Content-Type': 'application/cbor'},
      body: CBOR.encode({
        "id": assertion.id,
        "rawId": new Uint8Array(assertion.rawId),
        "authenticatorData": new Uint8Array(assertion.response.authenticatorData),
        "clientDataJSON": new Uint8Array(assertion.response.clientDataJSON),
        "signature": new Uint8Array(assertion.response.signature)
      })
    })
  }).then(function(response) {
    if (response.ok) {
      window.location = '/home';
    } else {
      alert('Authentication failed.');
    }
  }, function(reason) {
    console.log(reason.name);
    console.log(reason.message);
    alert(reason);
  });
}

function login_fido2_username(){
  let username = document.getElementById("username2").value;
  login_fido2(username);
  return false;
}

function login_fido2_rkey(){
  login_fido2();
  return false;
}
