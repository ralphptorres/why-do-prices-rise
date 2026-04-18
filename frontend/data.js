// sample price data for manila gas prices (january - april 2025)
const priceData = {
  labels: [
    'Jan 1', 'Jan 5', 'Jan 10', 'Jan 15', 'Jan 20', 'Jan 25', 'Jan 31',
    'Feb 5', 'Feb 10', 'Feb 15', 'Feb 20', 'Feb 28',
    'Mar 1', 'Mar 5', 'Mar 10', 'Mar 15', 'Mar 20', 'Mar 25', 'Mar 30',
    'Apr 5', 'Apr 10', 'Apr 15'
  ],
  prices: [
    55.20, 55.50, 56.10, 56.80, 57.20, 57.50, 58.00,
    58.30, 58.80, 59.20, 59.50, 60.20,
    60.50, 61.20, 62.80, 63.50, 65.30, 67.10, 68.95,
    70.50, 72.10, 74.20
  ],
  events: {
    'Jan 20': {
      title: 'israel continues gaza operations',
      description: 'tensions remain high in middle east',
      price_impact: 'up 0.7%',
      sources: [
        { name: 'Reuters', url: 'https://reuters.com' },
        { name: 'AP News', url: 'https://apnews.com' },
      ]
    },
    'Feb 15': {
      title: 'us warns iran over nuclear program',
      description: 'diplomatic tensions escalate',
      price_impact: 'up 0.9%',
      sources: [
        { name: 'AP News', url: 'https://apnews.com' },
        { name: 'Rappler', url: 'https://rappler.com' },
      ]
    },
    'Mar 10': {
      title: 'us airstrikes on iran',
      description: 'escalation in middle east tensions',
      price_impact: 'up 2.1%',
      sources: [
        { name: 'Reuters', url: 'https://reuters.com' },
        { name: 'AP News', url: 'https://apnews.com' },
      ]
    },
    'Mar 25': {
      title: 'iran retaliates with missiles',
      description: 'direct military response increases geopolitical risk',
      price_impact: 'up 1.8%',
      sources: [
        { name: 'Reuters', url: 'https://reuters.com' },
        { name: 'Rappler', url: 'https://rappler.com' },
        { name: 'Truth Social', url: 'https://truthsocial.com' },
      ]
    },
    'Apr 5': {
      title: 'oil supply concerns ease',
      description: 'temporary ceasefire reduces immediate market volatility',
      price_impact: 'up 0.8%',
      sources: [
        { name: 'Rappler', url: 'https://rappler.com' },
        { name: 'AP News', url: 'https://apnews.com' },
      ]
    },
    'Apr 15': {
      title: 'brent crude hits new high',
      description: 'ongoing geopolitical tensions maintain upward pressure',
      price_impact: 'up 1.2%',
      sources: [
        { name: 'Reuters', url: 'https://reuters.com' },
        { name: 'AP News', url: 'https://apnews.com' },
      ]
    }
  }
};
