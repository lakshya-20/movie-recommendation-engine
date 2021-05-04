<br />
<p align="center">

  <h3 align="center">Flick Movie Recommendation System</h3>

  <p align="center">
    Flick Movie Recommendation is a content-boosted recommendation system that provides users with movie recommendations based on their past interaction with the system.
    <br />
    <br />
    <a href="https://flick-frontend.herokuapp.com/">View Demo</a>
    ·
    <a href="https://github.com/lakshya-20/flick-frontend/issues">Report Bug</a>
    ·
    <a href="https://github.com/lakshya-20/flick-frontend/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The aim of this project is to build a web based application that will recommend movies to users that they might want to watch.
<br>
For this a content-boosted recommendation system is implemented that make use of ratings as well as comments to weight the recommendations. 

Here's why:
* The application only needs a web browser to work and can work on low-end devices.
* The application does not violet any legal requirement the user’s data is kept safe within the system as well as it does not violet any content laws.
* The application is working with an average latency of less than 100ms.

> Recommendation System folder have scripts for movie recommendation.
<br></br>
> Sentiment Analysis folder have scripts and model params for sentiment analysis (under development).

### Built With

* [Pandas](https://pandas.pydata.org/).
* [Numpy](https://numpy.org/)
* [Pymongo](https://pypi.org/project/pymongo/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python 3 >=3.4 [How to download python](https://www.python.org/downloads/)
* pip
  ```sh
  pip install --upgrade pip
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/<your_username>/flick.git
   ```
2. Go to Recommendation System folder and install dependencies
   ```sh
   pip install -r requirements.txt
   ```
   [Refer Documentation](https://pip.pypa.io/en/stable/cli/pip_install/#install-requirement)

   [Backend Repository](https://github.com/lakshya-20/flick-backend) 
   [Frontend Repository](https://github.com/lakshya-20/flick-frontend)
   

<!-- USAGE EXAMPLES -->
## Usage

In the project directory, you can run:
```sh
   python main.py
```
Server will start running at [http://localhost:5001](http://localhost:5001).

> [Live Demo Of the application](https://flick-frontend.herokuapp.com/)

## Contributing
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b some-new-feature`)
3. Commit your Changes (`git commit -m 'Add some feature'`)
4. In case of multiple commits squash them. [Refer documentation](https://www.internalpointers.com/post/squash-commits-into-one-git)
5. Push to the Branch (`git push origin some-new-feature`)
6. Open a Pull Request 

<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Lakshya Bansal - [lakshyabansal](https://www.linkedin.com/in/lakshyabansal/) 

Project Link: [https://github.com/lakshya-20/flick](https://github.com/lakshya-20/flick)

