export const useNavigation = (router) => {
  const navigateToHome = () => {
    router.push('/')
  }

  const navigateToLearnWildlife = () => {
    router.push('/learn-wildlife')
  }

  const navigateToSeasonal = () => {
    router.push('/seasonal')
  }

  const navigateToAIChallenge = () => {
    router.push('/ai-challenge')
  }

  const navigateToDailyWildle = () => {
    router.push('/daily-wildle')
  }

  const navigateToConservation = () => {
    router.push('/conservation')
  }

  return {
    navigateToHome,
    navigateToLearnWildlife,
    navigateToSeasonal,
    navigateToAIChallenge,
    navigateToDailyWildle,
    navigateToConservation
  }
}
