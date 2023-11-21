// const attributeValueStateMap = {
//   head_movement: { positive: "good", neutral: "mediocre", negative: "bad", "untested": "untested" },
//   gas_tank: { positive: "good", neutral: "mediocre", negative: "bad", "untested": "untested" },
//   aggression: { positive: "high", neutral: "mid", negative: "low", "untested": "untested" },
//   striking: { positive: "good", neutral: "mediocre", negative: "bad", "untested": "untested" },
//   chinny: { positive: "no", neutral: "somewhat", negative: "yes", "untested": "untested" },
//   desire_to_win: { positive: "yes", neutral: "kinda", negative: "no", "untested": "untested" },
//   grappling_offense: { positive: "good", neutral: "mediocre", negative: "bad", "untested": "untested" },
//   grappling_defense: { positive: "good", neutral: "mediocre", negative: "bad", "untested": "untested" }
// };

// const attribDescriptionMap = {
//   head_movement: {
//     positive: "doesn\'t stand upright/doesn't get hit unnecessarily",
//     neutral: "sometimes gets hit/keeps head upright",
//     negative: "gets hit alot/keeps head upright",
//   },
//   gas_tank: {
//     positive: "can go full 3 rounds without slowing down much",
//     neutral: "gets more tired but not entirely gassed",
//     negative: "after 1 or 2 rounds gassed and sloppy",
//   },
//   aggression: {
//     positive: "always moving forward, throwing strikes, looking for openings",
//     neutral: "sometimes moving forward, throwing strikes, looking for openings",
//     negative: "rarely moving forward/reactive not proactive fighter",
//   },
//   striking: {
//     positive: "uses all or most weapons kicks + punches + elbows + knees",
//     neutral: "mostly punches, not many or few kicks maybe proficient at boxing",
//     negative: "only punches/ maybe ok at boxing/ maybe sloppy striking",
//   },
//   chinny: {
//     positive: "can take hits and recover/ doesn't get ko'd",
//     neutral: "sometimes gets into trouble but has history of recovering",
//     negative: "history of getting ko'd/gets dazed or buzzed alot"
//   },
//   desire_to_win: {
//     positive: "always looking to win, tries to finish fight,never gives up",
//     neutral: "sometimes looking to win, sometimes looking to survive",
//     negative: "grindy fighter/ reactive not proactive fighter",
//   },
//   grappling_offense: {
//     positive: "tries to submit opponent/tries to get into dominant positions/tries to ground and pound",
//     neutral: "ok at takedowns, ok at submissions, ok at ground and pound",
//     negative: "loses position/overcommits to submissions and gets reversed",
//   },
//   grappling_defense: {
//     positive: "primarily can survive having back taken and not getting choked or submitted from difficult positions",
//     neutral: "ok at defending takedowns, ok at defending submissions, ok at defending ground and pound",
//     negative: "gets choked out/taps quickly/does wrong thing often",
//   },
// };
const attribInfoMap = {
  head_movement: {
    positive: { "description": "doesn't stand upright/doesn't get hit unnecessarily", "state": "good" },
    neutral: { "description": "sometimes gets hit/keeps head upright", "state": "mediocre" },
    negative: { "description": "gets hit alot/keeps head upright", "state": "bad" },
    untested: { "description": "untested", "state": "untested" }
  },
  gas_tank: {
    positive: { "description": "can go full 3 rounds without slowing down much", "state": "good" },
    neutral: { "description": "gets more tired but not entirely gassed", "state": "mediocre" },
    negative: { "description": "after 1 or 2 rounds gassed and sloppy", "state": "bad" },
    untested: { "description": "untested", "state": "untested" }
  },
  aggression: {
    positive: { "description": "always moving forward, throwing strikes, looking for openings", "state": "high" },
    neutral: { "description": "sometimes moving forward, throwing strikes, looking for openings", "state": "mid" },
    negative: { "description": "rarely moving forward/reactive not proactive fighter", "state": "low" },
    untested: { "description": "untested", "state": "untested" }
  },
  striking: {
    positive: { "description": "uses all or most weapons kicks + punches + elbows + knees", "state": "good" },
    neutral: { "description": "mostly punches, not many or few kicks maybe proficient at boxing", "state": "mediocre" },
    negative: { "description": "only punches/ maybe ok at boxing/ maybe sloppy striking", "state": "bad" },
    untested: { "description": "untested", "state": "untested" }
  },
  chinny: {
    positive: { "description": "can take hits and recover/ doesn't get ko'd", "state": "no" },
    neutral: { "description": "sometimes gets into trouble but has history of recovering", "state": "somewhat" },
    negative: { "description": "history of getting ko'd/gets dazed or buzzed alot", "state": "yes" },
    untested: { "description": "untested", "state": "untested" }
  },
  desire_to_win: {
    positive: { "description": "always looking to win, tries to finish fight,never gives up", "state": "yes" },
    neutral: { "description": "sometimes looking to win, sometimes looking to survive", "state": "kinda" },
    negative: { "description": "grindy fighter/ reactive not proactive fighter", "state": "no" },
    untested: { "description": "untested", "state": "untested" }
  },
  grappling_offense: {
    positive: {
      "description": "tries to submit opponent/tries to get into dominant positions/tries to ground and pound",
      "state": "good"
    },
    neutral: {
      "description": "ok at takedowns, ok at submissions, ok at ground and pound",
      "state": "mediocre"
    },
    negative: {
      "description": "loses position/overcommits to submissions and gets reversed",
      "state": "bad"
    },
    untested: {
      "description": "untested",
      "state": "untested"
    }
  },
  grappling_defense: {
    positive: {
      "description": "primarily can survive having back taken and not getting choked or submitted from difficult positions",
      "state": "good"
    },
    neutral: {
      "description": "ok at defending takedowns, ok at defending submissions, ok at defending ground and pound",
      "state": "mediocre"
    },
    negative: {
      "description": "gets choked out/taps quickly/does wrong thing often",
      "state": "bad"
    },
    untested: { "description": "untested", "state": "untested" }
  }
};