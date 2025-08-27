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
    neutral: { "description": "sometimes looking to win, sometimes looking to survive", "state": "somewhat" },
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

const attribCardOrder = [
  'head_movement',
  'gas_tank',
  'aggression',
  'desire_to_win',
  'striking',
  'chinny',
  'grappling_offense',
  'grappling_defense',
];

//on click attrib-edit-button show card body
const attribLabelValueMap = {
  'untested':0,
  'negative':1,
  'neutral':2,
  'positive':3
}
const attribValueLabelMap = {
  0:'untested',
  1:'negative',
  2:'neutral',
  3:'positive'
}

export default {
  install: (app,options) => {
    
    app.provide('attribInfoMap', attribInfoMap);
    app.provide('attribCardOrder', attribCardOrder);
    app.provide('attribLabelValueMap', attribLabelValueMap);
    app.provide('attribValueLabelMap', attribValueLabelMap);
  }
}