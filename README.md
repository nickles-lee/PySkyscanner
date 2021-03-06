# PySkyscanner Wrapper
This Python 2.x wrapper was written at KairosHacks in 2015, and has remained compatible despite additions and changes to Skyscanner’s REST API.

While this library is lacking in error handling, full coverage of the REST API, and being in pip, it can be helpful in getting a team started during a Hackathon or figuring out how to navigate some rather complicated and hefty API responses.

Simply put your API key into secrets.py, or manually specify it when instantiating your client.

## Files
* pySkyscanner.py provides a basic test application to orient oneself
* client.py provides a usable client that will wrap requests to the Skyscanner API, plus getters for relatively non-intuitive response objects

## Contact
If you have questions, feel free to raise an issue or contact me, and star this if you’ve found it useful. If it’s found useful, I’ll try to clean this up further in my spare time and this to the point where it can be put into a Python package repo.

[Skyscanner API Reference](https://skyscanner.github.io/slate/#flights-live-prices)
