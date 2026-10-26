# Explain it simply

Imagine a field has invisible colored patches underground. A laboratory sample tells you the concentration at exactly one spot. SoilQuest invents those fields and samples so you can compare sampling strategies without pretending a camera can detect metals. The model guesses between acquired samples and keeps track of where its guesses are uncertain. A sampling policy decides where to go next. The hidden answer is opened only for evaluation.

The robot moves on a square grid and cannot cross dark obstacle cells. Every step uses travel budget. Taking a sample uses sample budget. A long random walk can run out of travel before using all its sample slots. A regular grid can sometimes beat a clever-looking policy, especially when a narrow hotspot is easy to miss.

## Ten reviewer questions

1. Is any of this a real field measurement? No; all fields and observations are simulated.
2. Can a photo identify a metal? This application makes no such claim.
3. What is trained? A Gaussian-process length scale selected on training fields.
4. Can the policy see the answer? Its function receives only observations, geometry and GP predictions.
5. How is leakage tested? Changing hidden truth after observations does not change the model prediction.
6. Why compare several policies? Accuracy gains only matter relative to feasible alternatives.
7. Are sample counts identical? Ceilings are identical; travel exhaustion can reduce actual counts.
8. What do the uncertainty intervals mean? They describe this synthetic GP model, not proven real-soil confidence.
9. Where does it fail? Small unseen hotspots can remain undetected even with high aggregate interval coverage.
10. What is needed for real use? Actual lab measurements, georeferencing, soil chemistry expertise, calibrated transport models and external field validation.
