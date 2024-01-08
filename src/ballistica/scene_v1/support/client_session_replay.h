// Released under the MIT License. See LICENSE for details.

#ifndef BALLISTICA_SCENE_V1_SUPPORT_CLIENT_SESSION_REPLAY_H_
#define BALLISTICA_SCENE_V1_SUPPORT_CLIENT_SESSION_REPLAY_H_

#include <string>
#include <vector>

#include "ballistica/scene_v1/support/client_controller_interface.h"
#include "ballistica/scene_v1/support/client_session.h"

namespace ballistica::scene_v1 {

// A client-session fed by a replay file.
class ClientSessionReplay : public ClientSession,
                            public ClientControllerInterface {
 public:
  explicit ClientSessionReplay(std::string filename);
  ~ClientSessionReplay() override;
  void OnReset(bool rewind) override;

  // Our ClientControllerInterface implementation.
  auto GetActualTimeAdvanceMillisecs(double base_advance_millisecs)
      -> double override;
  void OnClientConnected(ConnectionToClient* c) override;
  void OnClientDisconnected(ConnectionToClient* c) override;
  void OnCommandBufferUnderrun() override;

  void Error(const std::string& description) override;
  void FetchMessages() override;
  void SaveState();
  void RestoreState(millisecs_t to_base_time);

 private:
  struct IntermediateState {
    // Message containing full scene state at the moment.
    std::vector<uint8_t> message_;
    std::vector<std::vector<uint8_t>> correction_messages_;

    // A position in replay file where we should continue from.
    long file_position_;

    millisecs_t base_time_;
  };

  void RestoreFromCurrentState();

  // List of passed states which we can rewind to.
  std::vector<IntermediateState> states_;
  IntermediateState current_state_;

  int unsaved_messages_count_{};

  uint32_t message_fetch_num_{};
  bool have_sent_client_message_{};
  std::vector<ConnectionToClient*> connections_to_clients_;
  std::vector<ConnectionToClient*> connections_to_clients_ignored_;
  std::string file_name_;
  FILE* file_{};
};

}  // namespace ballistica::scene_v1

#endif  // BALLISTICA_SCENE_V1_SUPPORT_CLIENT_SESSION_REPLAY_H_
