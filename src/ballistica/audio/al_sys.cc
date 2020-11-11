// Released under the MIT License. See LICENSE for details.

#include "ballistica/audio/al_sys.h"

#include "ballistica/audio/audio_server.h"
#include "ballistica/generic/utils.h"

// Need to move away from OpenAL on Apple stuff.
#if __clang__
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#endif

#if BA_ENABLE_AUDIO

namespace ballistica {

void _check_al_error(const char* file, int line) {
  if (g_audio_server->paused()) {
    Log(Utils::BaseName(file) + ":" + std::to_string(line)
        + ": Checking OpenAL error while paused.");
  }
  ALenum al_err = alGetError();
  if (al_err != AL_NO_ERROR) {
    Log(Utils::BaseName(file) + ":" + std::to_string(line)
        + ": OpenAL Error: " + GetALErrorString(al_err) + ";");
  }
}

auto GetALErrorString(ALenum err) -> const char* {
  static char undefErrStr[128];
#define DO_AL_ERR_CASE(a) \
  case a:                 \
    return #a
  switch (err) {
    DO_AL_ERR_CASE(AL_INVALID_NAME);
    DO_AL_ERR_CASE(AL_ILLEGAL_ENUM);
    DO_AL_ERR_CASE(AL_INVALID_VALUE);
    DO_AL_ERR_CASE(AL_ILLEGAL_COMMAND);
    DO_AL_ERR_CASE(AL_OUT_OF_MEMORY);
    default: {
      snprintf(undefErrStr, sizeof(undefErrStr), "(unrecognized: 0x%X (%d))",
               err, err);
      return undefErrStr;
    }
  }
#undef DO_AL_ERR_CASE
}

}  // namespace ballistica

#endif  // BA_ENABLE_AUDIO
