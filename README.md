[![MIT License][license-shield]][license-url]


## About The Project

xCapetime is a web platform that allows innovators and content creators to preserve unpublished work by creating NFTs with time-locks that will only unlock after a pre-determined time.

## Live Demo:

```text
https://xcapetime.herokuapp.com/
```

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

First clone the GitHub repository with:

* git
  ```sh
  git clone https://github.com/AleZadik/xCapeTime.git
  ```
  
* NFT.storage
  ```text
  Get an API key from https://nft.storage/
  ```
  
* Generate Fernet Encryption Key
  ```text
  Follow instructions here: https://cryptography.io/en/latest/fernet/
  ```
### Installation

_Below is an example of how to install and run the application._

1. Create an `.env` file and add the sample keys located in the `.local.env` file inside the `.env`. Make sure to include the Fernet key. For the file key, you can write a random string for now.
   ```text
     XCAPE_KEY=<YOUR_FERNET_ENCRYPTION_KEY>
     NFT_STORAGE_KEY=<YOUR_NFT_STORAGE_KEY>
     FILE_SECRET_KEY=ilkughdvnabm
     ENV=dev
     HOSTNAME=https://xcapetime.herokuapp.com
     LOCALHOST=127.0.0.1:8080
   ```
3. Install dependecies
   ```sh
   python3 -m pip install -r requirements.txt
   ```
3. Run Flask Server
   ```sh
   python3 main.py
   ```
4. Open Web Applicaiton
   ```text
   Open your browser and access 127.0.0.1:8080
   ```

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


[license-shield]: https://img.shields.io/github/license/AleZadik/xCapeTime?style=for-the-badge
[license-url]: https://github.com/AleZadik/xCapeTime/blob/main/LICENSE
